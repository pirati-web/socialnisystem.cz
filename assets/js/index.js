require('../sass/main.scss');
require('./smoothscroll');
const benefitCalculator = require('./parental-benefit-calculator');


function benefitClaimFormController(elem) {
    const container = elem.querySelector('.js-benefit-claim-form__container');
    const toggle = elem.querySelector('.js-benefit-claim-form__toggle');
    const toggleWrap = elem.querySelector('.js-benefit-claim-form__toggle-wrap');
    const divider = elem.querySelector('.js-benefit-claim-form__divider');

    toggle.addEventListener('click', evt => {
        evt.preventDefault();
        container.classList.remove('hide');
        toggleWrap.classList.add('hide');
        divider.classList.remove('hide');
    });
}


function homeScroll(elem) {
    elem.addEventListener('click', evt => {
        evt.preventDefault();
        const targetUrl = elem.getAttribute('href');
        const targetId = targetUrl.substring(1);
        const target = document.getElementById(targetId);
        window.scroll({top: target.offsetTop, behavior: 'smooth'});
        history.pushState({}, evt.target.text, targetUrl);
    });
}


const forEachNode = (nodelist, callback, scope) => {
    for (let i = 0; i < nodelist.length; i++) {
        callback.call(scope, i, nodelist[i]); // passes back stuff we need
    }
};

const handlers = [
    {query: '.js-benefit-claim-form.js-benefit-claim-form--submitted', handler: benefitClaimFormController},
    {query: '.js-smooth-scrollto', handler: homeScroll},
    {query: '.js-parental-benefit-calculator', handler: benefitCalculator},
];

handlers.forEach(handler => {
    forEachNode(document.querySelectorAll(handler.query), (index, rootElem) => {
        handler.handler(rootElem);
    });
});
