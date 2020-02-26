from urllib.parse import unquote
import scrapy
import re


class SegmentFaultSpider(scrapy.Spider):
    base_url = 'https://segmentfault.com'
    name = 'SegmentFaultSpider'
    start_urls = [
        'https://segmentfault.com/t/%E4%B8%83%E7%89%9B%E4%BA%91%E5%AD%98%E5%82%A8/blogs',
        'https://segmentfault.com/t/%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D/blogs',
        'https://segmentfault.com/t/%E4%BA%91%E6%9D%89%E7%BD%91%E7%BB%9C/blogs',
        'https://segmentfault.com/t/%E4%BA%91%E8%AE%A1%E7%AE%97/blogs',
        'https://segmentfault.com/t/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD/blogs',
        'https://segmentfault.com/t/%E4%BB%A5%E5%A4%AA%E5%9D%8A/blogs',
        'https://segmentfault.com/t/%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2/blogs',
        'https://segmentfault.com/t/%E5%8C%BA%E5%9D%97%E9%93%BE/blogs',
        'https://segmentfault.com/t/%E5%8F%88%E6%8B%8D%E4%BA%91%E5%AD%98%E5%82%A8/blogs',
        'https://segmentfault.com/t/%E5%A4%A7%E6%95%B0%E6%8D%AE/blogs',
        'https://segmentfault.com/t/%E5%A4%B4%E6%9D%A1%E5%B0%8F%E7%A8%8B%E5%BA%8F/blogs',
        'https://segmentfault.com/t/%E5%B0%8F%E7%A8%8B%E5%BA%8F%E4%BA%91%E5%BC%80%E5%8F%91/blogs',
        'https://segmentfault.com/t/%E5%B0%8F%E7%A8%8B%E5%BA%8F/blogs',
        'https://segmentfault.com/t/%E5%BE%AE%E4%BF%A1%E5%85%AC%E4%BC%97%E5%B9%B3%E5%8F%B0/blogs',
        'https://segmentfault.com/t/%E5%BE%AE%E4%BF%A1%E5%B0%8F%E7%A8%8B%E5%BA%8F/blogs',
        'https://segmentfault.com/t/%E5%BE%AE%E4%BF%A1%E5%BC%80%E5%8F%91%E8%80%85%E5%B7%A5%E5%85%B7/blogs',
        'https://segmentfault.com/t/%E5%BE%AE%E4%BF%A1%E5%BC%80%E6%94%BE%E5%B9%B3%E5%8F%B0/blogs',
        'https://segmentfault.com/t/%E5%BE%AE%E4%BF%A1/blogs',
        'https://segmentfault.com/t/%E6%90%9C%E7%B4%A2%E5%BC%95%E6%93%8E/blogs',
        'https://segmentfault.com/t/%E6%94%AF%E4%BB%98%E5%AE%9D%E5%B0%8F%E7%A8%8B%E5%BA%8F/blogs',
        'https://segmentfault.com/t/%E6%95%B0%E5%AD%97%E5%8C%96%E8%B4%A7%E5%B8%81/blogs',
        'https://segmentfault.com/t/%E6%95%B0%E6%8D%AE%E5%BA%93/blogs',
        'https://segmentfault.com/t/%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/blogs',
        'https://segmentfault.com/t/%E6%99%BA%E8%83%BD%E5%90%88%E7%BA%A6/blogs',
        'https://segmentfault.com/t/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0/blogs',
        'https://segmentfault.com/t/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F/blogs',
        'https://segmentfault.com/t/%E6%AF%94%E7%89%B9%E5%B8%81/blogs',
        'https://segmentfault.com/t/%E6%B6%9B%E6%80%9D%E6%95%B0%E6%8D%AE/blogs',
        'https://segmentfault.com/t/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/blogs',
        'https://segmentfault.com/t/%E7%81%B5%E9%9B%80%E4%BA%91/blogs',
        'https://segmentfault.com/t/%E7%99%BE%E5%BA%A6%E4%BA%91/blogs',
        'https://segmentfault.com/t/%E7%99%BE%E5%BA%A6%E6%99%BA%E8%83%BD%E5%B0%8F%E7%A8%8B%E5%BA%8F/blogs',
        'https://segmentfault.com/t/%E7%99%BE%E5%BA%A6/blogs',
        'https://segmentfault.com/t/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C/blogs',
        'https://segmentfault.com/t/%E7%BC%93%E5%AD%98/blogs',
        'https://segmentfault.com/t/%E7%BE%8E%E5%9B%A2%E4%BA%91/blogs',
        'https://segmentfault.com/t/%E8%85%BE%E8%AE%AF%E4%BA%91/blogs',
        'https://segmentfault.com/t/%E8%87%AA%E5%8A%A8%E9%A9%BE%E9%A9%B6/blogs',
        'https://segmentfault.com/t/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86/blogs',
        'https://segmentfault.com/t/%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1/blogs',
        'https://segmentfault.com/t/%E9%87%91%E5%B1%B1%E4%BA%91/blogs',
        'https://segmentfault.com/t/.net/blogs',
        'https://segmentfault.com/t/List/blogs',
        'https://segmentfault.com/t/actionscript/blogs',
        'https://segmentfault.com/t/ajax/blogs',
        'https://segmentfault.com/t/alauda/blogs',
        'https://segmentfault.com/t/amazon-web-services/blogs',
        'https://segmentfault.com/t/ambari/blogs',
        'https://segmentfault.com/t/analyzer/blogs',
        'https://segmentfault.com/t/android-studio/blogs',
        'https://segmentfault.com/t/android/blogs',
        'https://segmentfault.com/t/angular.js/blogs',
        'https://segmentfault.com/t/apache/blogs',
        'https://segmentfault.com/t/asp.net/blogs',
        'https://segmentfault.com/t/bash/blogs',
        'https://segmentfault.com/t/bootstrap/blogs',
        'https://segmentfault.com/t/bundle/blogs',
        'https://segmentfault.com/t/c%23/blogs',
        'https://segmentfault.com/t/c%2B%2B/blogs',
        'https://segmentfault.com/t/c/blogs',
        'https://segmentfault.com/t/centos/blogs',
        'https://segmentfault.com/t/chrome/blogs',
        'https://segmentfault.com/t/ci/blogs',
        'https://segmentfault.com/t/cloudera/blogs',
        'https://segmentfault.com/t/cocoa/blogs',
        'https://segmentfault.com/t/composer/blogs',
        'https://segmentfault.com/t/css/blogs',
        'https://segmentfault.com/t/css3/blogs',
        'https://segmentfault.com/t/deepflow/blogs',
        'https://segmentfault.com/t/django/blogs',
        'https://segmentfault.com/t/docker/blogs',
        'https://segmentfault.com/t/eclipse/blogs',
        'https://segmentfault.com/t/ecmascript/blogs',
        'https://segmentfault.com/t/elasticsearch/blogs',
        'https://segmentfault.com/t/emacs/blogs',
        'https://segmentfault.com/t/erlang/blogs',
        'https://segmentfault.com/t/facebook/blogs',
        'https://segmentfault.com/t/firefox/blogs',
        'https://segmentfault.com/t/flask/blogs',
        'https://segmentfault.com/t/flink/blogs',
        'https://segmentfault.com/t/flutter/blogs',
        'https://segmentfault.com/t/git/blogs',
        'https://segmentfault.com/t/github/blogs',
        'https://segmentfault.com/t/go/blogs',
        'https://segmentfault.com/t/golang/blogs',
        'https://segmentfault.com/t/hadoop/blogs',
        'https://segmentfault.com/t/hdfs/blogs',
        'https://segmentfault.com/t/hg/blogs',
        'https://segmentfault.com/t/hibernate/blogs',
        'https://segmentfault.com/t/hive/blogs',
        'https://segmentfault.com/t/html/blogs',
        'https://segmentfault.com/t/html5/blogs',
        'https://segmentfault.com/t/ico/blogs',
        'https://segmentfault.com/t/ide/blogs',
        'https://segmentfault.com/t/intellij-idea/blogs',
        'https://segmentfault.com/t/internet-explorer/blogs',
        'https://segmentfault.com/t/ios/blogs',
        'https://segmentfault.com/t/ipad/blogs',
        'https://segmentfault.com/t/iphone/blogs',
        'https://segmentfault.com/t/jar/blogs',
        'https://segmentfault.com/t/java-ee/blogs',
        'https://segmentfault.com/t/java/blogs',
        'https://segmentfault.com/t/javascript/blogs',
        'https://segmentfault.com/t/jquery/blogs',
        'https://segmentfault.com/t/json/blogs',
        'https://segmentfault.com/t/kafka/blogs',
        'https://segmentfault.com/t/kylin/blogs',
        'https://segmentfault.com/t/laravel/blogs',
        'https://segmentfault.com/t/linux/blogs',
        'https://segmentfault.com/t/lua/blogs',
        'https://segmentfault.com/t/lucene/blogs',
        'https://segmentfault.com/t/macos/blogs',
        'https://segmentfault.com/t/macosx/blogs',
        'https://segmentfault.com/t/mapreduce/blogs',
        'https://segmentfault.com/t/maven/blogs',
        'https://segmentfault.com/t/memcached/blogs',
        'https://segmentfault.com/t/microsoft/blogs',
        'https://segmentfault.com/t/mongodb/blogs',
        'https://segmentfault.com/t/mpvue/blogs',
        'https://segmentfault.com/t/mpx/blogs',
        'https://segmentfault.com/t/mvc/blogs',
        'https://segmentfault.com/t/mysql/blogs',
        'https://segmentfault.com/t/nginx/blogs',
        'https://segmentfault.com/t/node.js/blogs',
        'https://segmentfault.com/t/nosql/blogs',
        'https://segmentfault.com/t/objective-c/blogs',
        'https://segmentfault.com/t/oracle/blogs',
        'https://segmentfault.com/t/paddle/blogs',
        'https://segmentfault.com/t/perl/blogs',
        'https://segmentfault.com/t/phonegap/blogs',
        'https://segmentfault.com/t/php/blogs',
        'https://segmentfault.com/t/postgresql/blogs',
        'https://segmentfault.com/t/python/blogs',
        'https://segmentfault.com/t/react.js/blogs',
        'https://segmentfault.com/t/redis/blogs',
        'https://segmentfault.com/t/ruby-on-rails/blogs',
        'https://segmentfault.com/t/ruby/blogs',
        'https://segmentfault.com/t/rubygems/blogs',
        'https://segmentfault.com/t/rvm/blogs',
        'https://segmentfault.com/t/safari/blogs',
        'https://segmentfault.com/t/scala/blogs',
        'https://segmentfault.com/t/solr/blogs',
        'https://segmentfault.com/t/spark/blogs',
        'https://segmentfault.com/t/sphinx/blogs',
        'https://segmentfault.com/t/spring/blogs',
        'https://segmentfault.com/t/sql/blogs',
        'https://segmentfault.com/t/sqlalchemy/blogs',
        'https://segmentfault.com/t/sqlite/blogs',
        'https://segmentfault.com/t/sqoop/blogs',
        'https://segmentfault.com/t/struts/blogs',
        'https://segmentfault.com/t/sublime-text/blogs',
        'https://segmentfault.com/t/svn/blogs',
        'https://segmentfault.com/t/swift/blogs',
        'https://segmentfault.com/t/symfony/blogs',
        'https://segmentfault.com/t/talkingdata/blogs',
        'https://segmentfault.com/t/taro/blogs',
        'https://segmentfault.com/t/tdengine/blogs',
        'https://segmentfault.com/t/tensorflow/blogs',
        'https://segmentfault.com/t/textmate/blogs',
        'https://segmentfault.com/t/tomcat/blogs',
        'https://segmentfault.com/t/tornado/blogs',
        'https://segmentfault.com/t/twitter/blogs',
        'https://segmentfault.com/t/typescript/blogs',
        'https://segmentfault.com/t/ubuntu/blogs',
        'https://segmentfault.com/t/ucloud/blogs',
        'https://segmentfault.com/t/uni-app/blogs',
        'https://segmentfault.com/t/unix/blogs',
        'https://segmentfault.com/t/vim/blogs',
        'https://segmentfault.com/t/virtualenv/blogs',
        'https://segmentfault.com/t/visual-studio/blogs',
        'https://segmentfault.com/t/vue.js/blogs',
        'https://segmentfault.com/t/web.py/blogs',
        'https://segmentfault.com/t/webview/blogs',
        'https://segmentfault.com/t/wepy/blogs',
        'https://segmentfault.com/t/windows-server/blogs',
        'https://segmentfault.com/t/xcode/blogs',
        'https://segmentfault.com/t/xml/blogs',
        'https://segmentfault.com/t/zend-framework/blogs',
        'https://segmentfault.com/t/zookeeper/blogs'
    ]

    def parse(self, response):
        self.crawler.stats.set_value('spider_name', self.name)
        for row in response.xpath('//div[@id="blog"]//section//div[@class="summary"]'):
            title = row.xpath('.//h2//a/text()').extract_first()
            link = row.xpath('.//h2//a/@href').extract_first()
            tag = re.findall('/t/(.*?)/blogs', response.url)[0]
            tag = unquote(tag) if tag else None
            yield scrapy.Request(
                url=self.base_url + link,
                callback=self.parse_single,
                dont_filter=True,
                meta={'data': {'title': title, 'link': self.base_url + link, 'tag': tag}}
            )
        # 下一页
        next_link = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        print(next_link)
        if next_link:
            yield scrapy.Request(
                url=self.base_url + next_link,
                callback=self.parse,
                dont_filter=True,
            )

    def parse_single(self, response):
        author = response.xpath('//div[@id="sf-article_author"]//div//a//strong//text()').extract_first()
        # content = '\n'.join(response.xpath('//article//text()').extract())
        content = response.xpath('//article').extract_first()
        tmps = response.xpath('//div[@id="sf-article_metas"]//text()').extract()

        # 匹配阅读量 和 发布日期
        clicks = re.findall('\d+', tmps[0])
        if clicks:
            clicks = clicks[0]
        date = re.findall('\d+-\d+-\d+|\d+月\d+日', tmps[1])
        if date:
            date = date[0]
            if '月' in date:
                date = '2020-' + date.strip('日').replace('月', '-')
        res = {}
        res['website'] = self.base_url
        res['author'] = author
        # res['content'] = json.dumps({'text': content})
        res['content'] = content
        res['clicks'] = int(clicks)
        res['posted'] = date
        res.update(response.meta['data'])

        yield res
