/* appHeader */
var appHeader = new Vue({
    el: '#appHeader',
    data: {
        showSearchPanel: false,
        searchText: '',
        searchResult: [],
        hasResult: false,
        showNoResultMessage: false,
        showMobileNav: false
    },
    http: {
        root: '/'
    },
    watch: {
        searchText: function () {
            if (this.searchText.length > 2) {

                var self = this;
                var url = '/search?keyword=' + encodeURI(self.searchText);
                this.$http.get(url).then(
                    function (res) {
                        res = jsonVueResourceResponse(res);
                        var resBody = res.body;
                        var articles = resBody['articles'];
                        self.searchResult = [];
                        articles.forEach(function (item) {
                            self.searchResult.push({
                                link: '/post/' + item['id'],
                                publishTimeDisplay: item['publish_time_display'],
                                title: item['title']
                            })
                        })
                    },
                    function () {
                        self.searchResult = []
                    }
                ).then(
                    function () {
                        self.showNoResultMessage = ((!self.hasResult) && self.searchText.length > 2);
                    }
                )

            } else {
                this.searchResult = [];
                this.showNoResultMessage = ((!this.hasResult) && this.searchText.length > 2);
            }
        },
        showSearchPanel: function () {
            if (this.showSearchPanel) {
                this.searchText = '';
            }
        },
        searchResult: function () {
            this.hasResult = (this.searchResult.length != 0);
        }
    }
});

/* appFooter */
var appFooter = new Vue({
    el: '#appFooter',
    data: {
        showBackToTop: false,
        copyrightYear: new Date().getFullYear()
    }
});

/* appHome */
var appHome = new Vue({
    el: '#appHome',
    data: {
        loading: false,
        articles: [],
        pageNum: 0,
        tagId: 0,
        hasMoreArticle: true
    },
    http: {
        root: '/'
    },
    created: function () {
        setTimeout('appHome.loadMoreData()', 100);
    },
    methods: {
        loadMoreData: function () {
            var self = this;
            if (self.loading || !self.hasMoreArticle) {
                return;
            }
            self.loading = true;
            var url = '/post?page_num=' + (self.pageNum + 1) + '&page_size=5&tag_id=' + self.tagId;
            this.$http.get(url).then(
                function (res) {
                    res = jsonVueResourceResponse(res);
                    var resBody = res.body;
                    self.pageNum = resBody['page_num'];
                    var articles = resBody['articles'];
                    if (articles.length == 0) {
                        self.hasMoreArticle = false;
                        return;
                    }
                    articles.forEach(function (articleItem) {
                        var article = Object();
                        article.link = '/post/' + articleItem['id'];
                        article.title = articleItem['title'];
                        article.publishTimeDisplay = articleItem['publish_time_display'];
                        article.previewContent = articleItem['preview_content'];
                        article.hasBGM = articleItem['bgm_id'] != null && articleItem['bgm_id'] != '';
                        article.tags = [];
                        var tagList = articleItem['tags'];
                        tagList.forEach(function (tagItem) {
                            var tag = Object();
                            tag.title = tagItem['title'];
                            article.tags.push(tag);
                        });
                        article.images = [];
                        var imageList = articleItem['images'];
                        imageList.forEach(function (imageItem) {
                           var image = Object();
                            image.id = imageItem['id'];
                            image.url = imageItem['url'];
                            article.images.push(image);
                        });
                        self.articles.push(article);
                    });
                },
                function () {
                }
            ).then(
                function () {
                    self.loading = false;
                }
            )
        }
    },
    watch: {
        tagId: function () {
            this.articles = [];
            this.pageNum = 0;
            this.hasMoreArticle = true;
            this.loadMoreData();
        }
    }
});

/* appAbout */
var appAbout = new Vue({
    el: '#appAbout',
    data: {}
});

/*
 * Convert body of vue response to json object
 */
jsonVueResourceResponse = function (res) {
    var contentType = res.bodyBlob.type;
    if (contentType != 'application/json') {
        res.body = JSON.parse(res.body);
    }
    return res;
};

/*
 * Smooth move to top
 */
var movingUp = false;
var movingOffset = 0;
var movingSwitchLine = 0;
smoothMoveUp = function () {

    if (!movingUp) {
        movingSwitchLine = (document.body.scrollTop || document.documentElement.scrollTop) / 3;
    }

    movingUp = true;

    if ((document.body.scrollTop || document.documentElement.scrollTop) >= (20 + movingOffset)) {
        document.body.scrollTop -= 20 + movingOffset;
        document.documentElement.scrollTop -= 20 + movingOffset;
        if ((document.body.scrollTop || document.documentElement.scrollTop) >= movingSwitchLine) {
            movingOffset = movingOffset + 5;
        } else {
            movingOffset = movingOffset - 5;
        }
        setTimeout('smoothMoveUp()', 5);
    } else {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
        movingUp = false;
        movingOffset = 0;
        movingSwitchLine = 0;
        appFooter.showBackToTop = false;
    }

};

