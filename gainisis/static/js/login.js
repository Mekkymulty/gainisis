
// Login
let lgncheck = document.getElementById('lgncheck');
lgncheck.onchange = () => {
    lgncheck.checked ? document.getElementById('lgnpsw').type = 'text' : document.getElementById('lgnpsw').type = 'password';
};

