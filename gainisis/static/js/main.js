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
function dshShare() {
    navigator.share({
        title: document.title,
        // text: "Hello World",
        text: document.getElementById('userref').innerHTML,
        url: window.location.href
    })
    // .then(() => console.log('Successful share'))
    // .catch(error => console.log('Error sharing:', error));
};
function dshCpyWal() {
    const ivst = document.createRange();
    ivst.selectNode(document.getElementById('userref'));
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(ivst);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
};

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



// invest
let ivstnetwork = document.querySelector("#ivstnetwork");
ivstnetwork.addEventListener('input', () => {
    if (ivstnetwork.value >= 50) {
        document.getElementById('lowerval').classList.replace('d-block','d-none')
    };
});
let dpstSubmit = document.querySelector("#deposit-submit");
dpstSubmit.addEventListener('click', (e) => {
    e.preventDefault();
    if (ivstnetwork.value >= 50) {
        document.forms['netw_subm'].submit();
    } else {
        document.getElementById('lowerval').classList.replace('d-none','d-block')
    };
});

function BTCwalCopy() {
    const ivst = document.createRange();
    ivst.selectNode(document.getElementById('btc-deposit-wal'));
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(ivst);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
};
function ETHwalCopy() {
    const ivst = document.createRange();
    ivst.selectNode(document.getElementById('eth-deposit-wal'));
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(ivst);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
};
function DOGEwalCopyz() {
    const ivst = document.createRange();
    ivst.selectNode(document.getElementById('doge-deposit-wal'));
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(ivst);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
};
function LTCwalCopy() {
    const ivst = document.createRange();
    ivst.selectNode(document.getElementById('ltc-deposit-wal'));
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(ivst);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
};



// ''''' PLANS '''''
// bronze
let bronzeform = document.querySelector("#bronzeform");
bronzeform.addEventListener('input', () => {
    alert('rtyuio')
    if (bronzeform.value >= 50 && bronzeform.value <= 499) {
        document.getElementById('bronzeval').classList.replace('d-block','d-none')
    };
});
let bronzesubmit = document.querySelector("#bronzesubmit");
bronzesubmit.addEventListener('click', (e) => {
    e.preventDefault();
    if (bronzeform.value >= 50 && bronzeform.value <= 499) {
        document.forms['bronzeform'].submit();
    } else {
        document.getElementById('bronzeval').classList.replace('d-none','d-block')
    };
});
// silver
let silverform = document.querySelector("#silverform");
silverform.addEventListener('input', () => {
    if (silverform.value >= 500 && silverform.value <= 999) {
        document.getElementById('silverval').classList.replace('d-block','d-none')
    };
});
let silversubmit = document.querySelector("#silversubmit");
silversubmit.addEventListener('click', (e) => {
    e.preventDefault();
    if (silverform.value >= 500 && silverform.value <= 999) {
        document.forms['silverform'].submit();
    } else {
        document.getElementById('silverval').classList.replace('d-none','d-block')
    };
});
// gold
let goldform = document.querySelector("#goldform");
goldform.addEventListener('input', () => {
    if (goldform.value >= 1000 && goldform.value >= 9999) {
        document.getElementById('doldval').classList.replace('d-block','d-none')
    };
});
let goldsubmit = document.querySelector("#goldsubmit");
goldsubmit.addEventListener('click', (e) => {
    e.preventDefault();
    if (goldform.value >= 1000 && goldform.value >= 9999) {
        document.forms['goldform'].submit();
    } else {
        document.getElementById('doldval').classList.replace('d-none','d-block')
    };
});
// platinum
let platinumform = document.querySelector("#platinumform");
platinumform.addEventListener('input', () => {
    if (platinumform.value >= 10000 && platinumform.value >= 49000) {
        document.getElementById('platinumval').classList.replace('d-block','d-none')
    };
});
let platinumsubmit = document.querySelector("#platinumsubmit");
platinumsubmit.addEventListener('click', (e) => {
    e.preventDefault();
    if (platinumform.value >= 10000 && platinumform.value >= 49000) {
        document.forms['platinumform'].submit();
    } else {
        document.getElementById('platinumval').classList.replace('d-none','d-block')
    };
});
// sapphire
let sapphireform = document.querySelector("#sapphireform");
sapphireform.addEventListener('input', () => {
    if (sapphireform.value >= 50000 && sapphireform.value >= 99999) {
        document.getElementById('sapphireval').classList.replace('d-block','d-none')
    };
});
let sapphiresubmit = document.querySelector("#sapphiresubmit");
sapphiresubmit.addEventListener('click', (e) => {
    e.preventDefault();
    if (sapphireform.value >= 50000 && sapphireform.value >= 99999) {
        document.forms['sapphireform'].submit();
    } else {
        document.getElementById('sapphireval').classList.replace('d-none','d-block')
    };
});
// diamond
let diamondform = document.querySelector("#diamondform");
diamondform.addEventListener('input', () => {
    if (diamondform.value >= 100000 && diamondform.value >= 500000) {
        document.getElementById('diamondval').classList.replace('d-block','d-none')
    };
});
let diamondsubmit = document.querySelector("#diamondsubmit");
diamondsubmit.addEventListener('click', (e) => {
    e.preventDefault();
    if (diamondform.value >= 100000 && diamondform.value >= 500000) {
        document.forms['diamondform'].submit();
    } else {
        document.getElementById('diamondval').classList.replace('d-none','d-block')
    };
});


// Support
function supportOpen() {
    document.getElementById('support').classList.replace('d-none', 'd-block')
};
function supportClose() {
    document.getElementById('support').classList.replace('d-block', 'd-none')
};
function supportSend() {
    if (document.getElementById('user_email').value.length > 0 && document.getElementById('support_message').value.length > 0) {
        var email = 'gainisis2@gmail.com'
        var subject = "Email support";
        var variableList = document.getElementById('support_message').value;
        var body = variableList == "Other" ? document.getElementById("newVariable").value : variableList;
        window.location = "mailto:" + email + "?subject=" + subject + "&body=" + body;
    };
};




// Footer
const year = new Date();
var yearDate =  year.getFullYear();
window.onload = () => {
    document.getElementById('comyear').innerHTML = yearDate;
};


