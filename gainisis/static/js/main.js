// Language Selector
// function changeLanguage(lang) {
//     let element = document.getElementById('index');
//     if (lang == 'en') {
//         element.innerHTML = 'English o!'
//     };
//     if (lang == 'fr') {
//         element.innerHTML = 'French o!'
//     };
//     if (lang == 'de') {
//         element.innerHTML = 'German o!'
//     };
// };


// Nav Bar
let nvmenubtn = document.getElementsByClassName("nvmenubtn");
let activepage = document.getElementsByClassName("activepage");
for (let i = 0; i < activepage.length; i++) {
    activepage[i].addEventListener("mouseover", function() {
        if (this.classList.contains('actindex')) {
            nvmenubtn[0].classList.add('navactive');
        };
        if (this.classList.contains('actdashboard')) {
            nvmenubtn[1].classList.add('navactive');
        };
        if (this.classList.contains('actinvest')) {
            nvmenubtn[2].classList.add('navactive');
        };
        if (this.classList.contains('actwithdraw')) {
            nvmenubtn[3].classList.add('navactive');
        };
    });
    activepage[i].addEventListener("touchstart", function() {
        if (this.classList.contains('actindex')) {
            nvmenubtn[0].classList.add('navactive');
        };
        if (this.classList.contains('actdashboard')) {
            nvmenubtn[1].classList.add('navactive');
        };
        if (this.classList.contains('actinvest')) {
            nvmenubtn[2].classList.add('navactive');
        };
        if (this.classList.contains('actwithdraw')) {
            nvmenubtn[3].classList.add('navactive');
        };
    });
    
    activepage[i].addEventListener("click", function() {
        const alert_close = document.querySelector('.alert_close');
        if (this.classList.contains('actindex') ||
            this.classList.contains('actdashboard') ||
            this.classList.contains('actinvest') ||
            this.classList.contains('actwithdraw')) {
                alert_close.click();
        };
    });
};




// Index
document.addEventListener("DOMContentLoaded", function() {
    var body_scroll = document.querySelector('#body_scroll');
    body_scroll.addEventListener('scroll', function() {
        if (body_scroll.scrollTop > 60) {
            navbar_height = document.querySelector('.navbar').offsetHeight;
            body_scroll.style.paddingTop = navbar_height + 'px';
            document.getElementById('navbar_top').classList.add('fixed-top', 'border-bottom');
        } else {
            body_scroll.style.paddingTop = '0';
            document.getElementById('navbar_top').classList.remove('fixed-top', 'border-bottom');
        };
    });
});


// Dashboard
// function dshCpyWal() {
//     const ivst = document.createRange();
//     ivst.selectNode(document.getElementById('userref'));
//     window.getSelection().removeAllRanges();
//     window.getSelection().addRange(ivst);
//     document.execCommand('copy');
//     window.getSelection().removeAllRanges();
// };

// btc wal
let showWalIpt = document.getElementsByClassName("showwalipt");
var dshsbmtwal = document.getElementById('dshsbmtwal');
let walcncl = document.getElementById('walcncl');
walIpt = Array.from(showWalIpt);
walIpt.forEach((elem) => {
    elem.addEventListener('click', () => {
        elem.classList.add('d-none');
        dshsbmtwal.classList.replace("d-none", "d-block");
        ethWalcncl.click();
        walDgCncl.click();
    });
    
    walcncl.onclick = () => {
        elem.classList.remove('d-none');
        dshsbmtwal.classList.replace("d-block", "d-none");
    };
});
// eth wal
let showEthWal = document.getElementsByClassName("showethwalipt");
var dshEthWal = document.getElementById('dshsbmtethwal');
let ethWalcncl = document.getElementById('ethwalcncl');
ethIpt = Array.from(showEthWal);
ethIpt.forEach((elem) => {
    elem.addEventListener('click', () => {
        elem.classList.add('d-none');
        dshEthWal.classList.replace("d-none", "d-block");
        walcncl.click();
        walDgCncl.click();
    });
    
    ethWalcncl.onclick = () => {
        elem.classList.remove('d-none');
        dshEthWal.classList.replace("d-block", "d-none");
    };
});
// dodge wal
let shDodgeWal = document.getElementsByClassName("shdodgewal");
var dshDodgeWal = document.getElementById('dshdodgewal');
let walDgCncl = document.getElementById('waldgcncl');
dgIpt = Array.from(shDodgeWal);
dgIpt.forEach((elem) => {
    elem.addEventListener('click', () => {
        elem.classList.add('d-none');
        dshDodgeWal.classList.replace("d-none", "d-block");
        walcncl.click();
        ethWalcncl.click();
    });
    
    walDgCncl.onclick = () => {
        elem.classList.remove('d-none');
        dshDodgeWal.classList.replace("d-block", "d-none");
    };
});
// lite wal
let shwltewal = document.getElementsByClassName("shwltewal");
var dshblteform = document.getElementById('dshblteform');
let walltecncl = document.getElementById('walltecncl');
walLte = Array.from(shwltewal);
walLte.forEach((elem) => {
    elem.addEventListener('click', () => {
        elem.classList.add('d-none');
        dshblteform.classList.replace("d-none", "d-block");
        walcncl.click();
        ethWalcncl.click();
    });
    
    walltecncl.onclick = () => {
        elem.classList.remove('d-none');
        dshblteform.classList.replace("d-block", "d-none");
    };
});

let tranStat = document.getElementsByClassName("tran-stat");
tStt = Array.from(tranStat);
tStt.forEach((elem) => {
    window.onload = () => {
        if (elem.innerHTML == 'Successful') {elem.classList.add('text-success');};
        if (elem.innerHTML == 'Pending') {elem.classList.add('text-warning');};
        if (elem.innerHTML == 'Failed') {elem.classList.add('text-danger');};
    };
});


// invest
let ivstNetwork = document.getElementsByClassName("ivstnetwork");
walNwt = Array.from(ivstNetwork);
walNwt.forEach((elem) => {
    elem.addEventListener('click', () => {
        document.forms['netw_subm'].submit();
    });
});

function ivstCpyWal() {
    const ivst = document.createRange();
    ivst.selectNode(document.getElementById('invwal'));
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(ivst);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
};



// Footer
const year = new Date();
var yearDate =  year.getFullYear();
window.onload = () => {
    document.getElementById('comyear').innerHTML = yearDate;
};
// support
let supportBtn = document.querySelector('#support-btn');
supportBtn.addEventListener('click', () => {
    document.getElementById('support').classList.replace('d-none', 'd-block');
});
let supportClose = document.querySelectorAll('.sprt_close, #nav_sprt');
supportClose.addEventListener('click', () => {
    document.getElementById('support').classList.replace('d-block', 'd-none');
});


