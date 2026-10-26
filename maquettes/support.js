/*
 * UrbanSignal — mini moteur de rendu pour ouvrir les maquettes (.dc.html)
 * directement dans un navigateur, sans serveur.
 *
 * Gère : {{chemin.pointé}} dans le texte et les attributs, <sc-for>, <sc-if>,
 * <helmet>, les attributs on* (onClick, onChange…) et la classe Component
 * (state, setState, renderVals) déclarée dans <script type="text/x-dc">.
 */
(function () {
  var hide = document.createElement('style');
  hide.textContent = 'x-dc{display:none!important}';
  document.head.appendChild(hide);

  var HOLE = /\{\{\s*([^}]*?)\s*\}\}/g;
  var FULL = /^\{\{\s*([^}]*?)\s*\}\}$/;
  var BOOL_ATTRS = { checked: 1, disabled: 1, selected: 1, hidden: 1, readonly: 1, required: 1 };

  function DCLogic(props) {
    this.props = props || {};
    this.state = {};
  }
  DCLogic.prototype.setState = function (patch) {
    var next = typeof patch === 'function' ? patch(this.state, this.props) : patch;
    this.state = Object.assign({}, this.state, next);
    if (this.__render) this.__render();
  };
  window.DCLogic = DCLogic;

  function lookup(path, scopes) {
    if (path === 'true') return true;
    if (path === 'false') return false;
    if (path === 'null' || path === '') return null;
    var parts = path.split('.');
    for (var i = scopes.length - 1; i >= 0; i--) {
      if (scopes[i] && parts[0] in scopes[i]) {
        var v = scopes[i][parts[0]];
        for (var j = 1; j < parts.length && v != null; j++) v = v[parts[j]];
        return v;
      }
    }
    return undefined;
  }

  function str(v) {
    return v == null || v === false ? '' : String(v);
  }

  function interpolate(text, scopes) {
    return text.replace(HOLE, function (_, p) { return str(lookup(p, scopes)); });
  }

  function processAttrs(el, scopes) {
    Array.prototype.slice.call(el.attributes).forEach(function (a) {
      var name = a.name, value = a.value;
      if (name.indexOf('hint-') === 0) { el.removeAttribute(name); return; }
      if (value.indexOf('{{') === -1) return;
      var full = value.match(FULL);
      if (name.indexOf('on') === 0) {
        el.removeAttribute(name);
        var fn = full && lookup(full[1], scopes);
        if (typeof fn !== 'function') return;
        var type = name.slice(2).toLowerCase();
        if (type === 'change' && el.tagName === 'INPUT' && /^(text|search|email|number|tel|url|password)$/.test(el.type)) type = 'input';
        el.addEventListener(type, fn);
        return;
      }
      if (full && BOOL_ATTRS[name]) {
        var on = !!lookup(full[1], scopes);
        if (on) el.setAttribute(name, ''); else el.removeAttribute(name);
        if (name in el) el[name] = on;
        return;
      }
      if (full) {
        var v = lookup(full[1], scopes);
        if (v == null || v === false) el.removeAttribute(name);
        else el.setAttribute(name, String(v));
        return;
      }
      el.setAttribute(name, interpolate(value, scopes));
    });
  }

  // Rend les enfants de `src` (fragment de template) dans `out` avec les portées `scopes`.
  function renderChildren(src, out, scopes, head) {
    Array.prototype.forEach.call(src.childNodes, function (node) {
      if (node.nodeType === 3) {
        out.appendChild(document.createTextNode(interpolate(node.nodeValue, scopes)));
        return;
      }
      if (node.nodeType !== 1) return;
      var tag = node.tagName.toLowerCase();
      if (tag === 'helmet') {
        if (head) renderChildren(node, head, scopes, null);
        return;
      }
      if (tag === 'sc-for') {
        var m = (node.getAttribute('list') || '').match(FULL);
        var list = m ? lookup(m[1], scopes) : null;
        var as = node.getAttribute('as') || 'item';
        (Array.isArray(list) ? list : []).forEach(function (item, index) {
          var scope = {}; scope[as] = item; scope.index = index;
          renderChildren(node, out, scopes.concat([scope]), head);
        });
        return;
      }
      if (tag === 'sc-if') {
        var c = (node.getAttribute('value') || '').match(FULL);
        if (c && lookup(c[1], scopes)) renderChildren(node, out, scopes, head);
        return;
      }
      var el = document.importNode(node, false);
      processAttrs(el, scopes);
      var content = tag === 'template' ? node.content : node;
      renderChildren(content, tag === 'template' ? el.content : el, scopes, head);
      out.appendChild(el);
    });
  }

  function boot() {
    var host = document.querySelector('x-dc');
    if (!host) return;
    var tpl = document.createElement('template');
    tpl.innerHTML = host.innerHTML;
    host.parentNode.removeChild(host);

    var script = document.querySelector('script[data-dc-script]');
    var props = {};
    var Component = null;
    if (script) {
      try { props = JSON.parse(script.getAttribute('data-props') || '{}'); } catch (e) { props = {}; }
      Component = new Function('DCLogic', script.textContent + '\n;return typeof Component !== "undefined" ? Component : null;')(DCLogic);
    }
    var logic = Component ? new Component(props) : new DCLogic(props);

    var root = document.createElement('div');
    root.setAttribute('data-dc-root', '');
    document.body.insertBefore(root, document.body.firstChild);

    var headDone = false;
    logic.__render = function () {
      var vals = typeof logic.renderVals === 'function' ? logic.renderVals() || {} : {};
      var frag = document.createDocumentFragment();
      renderChildren(tpl.content, frag, [vals], headDone ? null : document.head);
      headDone = true;
      root.replaceChildren(frag);
    };
    logic.__render();

    if (location.hash) {
      var target = document.getElementById(location.hash.slice(1));
      if (target) target.scrollIntoView();
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
