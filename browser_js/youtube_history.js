// Prints a list of <video-title>;;<video-url>;;<video-thumbnail-url> of videos from your YouTube history page.
//   Also prints 'Group Header' lines at the start of each days' video groups (i.e. Group Header: Jun 20).

function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
}

function getRelativeElementByXpath(path, root) {
return document.evaluate(path, root, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
}

content_node = getElementByXpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[2]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]')

groups = [];
for (var iday_group = 0; iday_group < content_node.children.length; ++iday_group) {
    day_group = content_node.children[iday_group];
    if (day_group.tagName === "YTD-ITEM-SECTION-RENDERER") {
        group_header = getRelativeElementByXpath("div[1]/ytd-item-section-header-renderer/div/div", day_group).innerText;

        group_videos = [];
        for(var inode = 0; inode < getRelativeElementByXpath("div[3]", day_group).children.length; ++inode) {
            video_node = getRelativeElementByXpath("div[3]", day_group).children[inode];
            if (video_node.tagName == "YTD-VIDEO-RENDERER") {
                thumbnail_node = getRelativeElementByXpath("div[1]/ytd-thumbnail/a/yt-image", video_node);
                title_node = getRelativeElementByXpath("div[1]/div/div[1]/div/h3/a", video_node);
                url_node = getRelativeElementByXpath("div[1]/ytd-thumbnail/a", video_node);
                
                thumbnail = thumbnail_node.data.thumbnails[0].url;
                title = title_node.innerText;
                url = url_node.href;

                group_videos = group_videos.concat([{'title': title, 'thumbnail': thumbnail, 'url': url}]);
            }
        }

        groups = groups.concat([{'header': group_header, 'videos': group_videos}]);
    }
}

//console.log(groups);

for(var ig = 0; ig < groups.length; ++ig) {
    console.log('Group Header: ' + groups[ig].header);
    for(var iv = 0; iv < groups[ig].videos.length; ++iv) {
        console.log(groups[ig].videos[iv].title + ';;' + groups[ig].videos[iv].url + ';;' + groups[ig].videos[iv].thumbnail);
    };
}
