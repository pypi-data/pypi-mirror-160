
try {
    new Function("import('/reactfiles/frontend/main.85864713.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main.85864713.js';
    el.type = 'module';
    document.body.appendChild(el);
}
