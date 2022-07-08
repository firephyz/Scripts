function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
}

for (let i = 0; i < 121; ++i) {
    a = getElementByXpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[' + (i+1) + ']/div[1]/div[1]/div[1]/h3/a');
    console.log(a.innerHTML + ';;' + a.href);
}
