# Application Dashboard

This application provides all usrs to view and seatch function.


## Basic URL Structures

| URI | Usage |
|-----|-------------|
| `^dashboard/$`              |  Root URI of this application |
| `^/dashboard/view/$`        | List view |
| `^/dashboard/view/list/$`   | List view |
| `^/dashboard/view/bibtex/$` | Bibtex style view |
| `^/dashboard/view/table/$`  | Table style view  |
| `^/dashboard/view/tile/$`   | Tile style view   |


## How to Edit Display Style
To change display style {List, Table, Bibtex, Latex}, plsease edit the function in `dashboard/templatetags/utils_bib_fomrat.py`. We provide call back function (implemented as Class Object) for several display formats. When you want to change the style, just overwrite  the `get_template_{TEMPLATE STYLE}` functions.

```python
# Example of Template tag function.
# ---------------------------------

class BibtexFormatListDefault(BibtexFormatBase):

    def get_template_INTPROC(self):
        html = (
            '{authors}; '
            '<a href="{url_bib}">"{title}"</a>, '
            '2017'
        )
        return html    

    def get_template_JOURNAL(self):
        html = (
            '{authors}; '
            '<a href="{url_bib}">"{title}"</a>, '
            '2017 '
            '(JOURNAL)'
        )
        return html
```

### Default Style Examples
#### List Style
```
dashboard.templatetags.utils_bib_format.BibtexFormatListDefault
```

#### International Proceedings

+ Bibtex View
```
@inproceedings{<id>,
         title = {<title_en>},
        author = {<authors_en>},
     booktitle = {<book>},
        volume = {<volume>},
        number = {<number>},
         pages = {<page>},
         month = {<pub_date[1]>},
          year = {<pub_date[0]>},
}
```
```
@inproceedings{id2754,
         title = {Monitoring Range Motif on Streaming Time-Series},
        author = {Shinya Kato and Daichi Amagata and Shunya Nishio and Takahiro Hara},
     booktitle = {International Conference on Database and Expert Systems Applications (DEXA 2018)},
        volume = {1},
        number = {1},
         pages = {251-266},
         month = {9},
          year = {2018},
}
```

+ List View
```
[1] <authors_en>, "<title_en>," <book>, volume <volume>, number <number>, pages <page> <pub_date[1]> <pub_date[0]>.
```
```
[1] Shinya Kato and Daichi Amagata and Shunya Nishio and Takahiro Hara, "Monitoring Range Motif on Streaming Time-Series," International Conference on Database and Expert Systems Applications (DEXA 2018), volume 1, number 1, pages 251-266 September 2018.
```

+ Table View

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|type|book|authors|title_en|pub_date[0]年 pub_date[1]月|link|

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|国際会議|International Conference on Database and Expert Systems Applications (DEXA 2018)|Shinya Kato and Daichi Amagata and Shunya Nishio and Takahiro Hara|Monitoring Range Motif on Streaming Time-Series|2018年9月|link|


#### Journal Paper

+ Bibtex View
```
@article{<id>,
         title = {<title_en>},
        author = {<authors_en>},
       journal = {<book>},
        volume = {<volume>},
        number = {<number>},
         pages = {<page>},
         month = {<pub_date[1]>},
          year = {<pub_date[0]>},
}
```
```
@article{id2741,
         title = {Privacy-Preserving Recognition of Object-based Activities Using Near-Infrared Reflective Markers},
        author = {Joseph Korpela and Takuya Maekawa},
     journal = {ACM/Springer Personal and Ubiquitous Computing (ACM/Springer PUC)},
        volume = {22},
        number = {2},
         pages = {365-377},
         month = {4},
          year = {2018},
}
```

+ List View
```
[1] <authors_en>, "<title_en>," <book>, volume <volume>, number <number>, pages <page> <pub_date[1]> <pub_date[0]>.
```
```
[1]Joseph Korpela and Takuya Maekawa, "Privacy-Preserving Recognition of Object-Based Activities Using Near-Infrared Reflective Markers," ACM/Springer Personal and Ubiquitous Computing (ACM/Springer PUC), volume 22, number 2, pages 365-377 April 2018.
```

+ Table View

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|type|book|authors|title_en|pub_date[0]年 pub_date[1]月|link|

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|論文誌|ACM/Springer Personal and Ubiquitous Computing (ACM/Springer PUC)|J. Korpela and T. Maekawa|Privacy-Preserving Recognition of Object-Based Activities Using Near-Infrared Reflective Markers|2018年4月|link|


#### Domestic Conference(査読付き)

+ Bibtex View
```
@inproceedings{<id>,
         title = {<title_ja>or<title_en>},
        author = {<authors_ja>},
     booktitle = {<book>},
        volume = {<volume>},
        number = {<number>},
         pages = {<page>},
         month = {<pub_date[1]>},
          year = {<pub_date[0]>},
}
```
```
@inproceedings{id2753,
         title = {ストリーミング時系列データの効率的なモチーフモニタリングアルゴリズム},
        author = {加藤 慎也 and 天方 大地 and 西尾 俊哉 and 原 隆浩},
     booktitle = {情報処理学会マルチメディア，分散，協調とモバイル(DICOMO2018)シンポジウム論文集},
         pages = {1473-1480},
         month = {7},
          year = {2018},
}
```

+ List View
```
[1] <authors_ja>, "<title_ja>or<title_en>," <book>, pages <page> <pub_date[0]>年<pub_date[1]>月 .
```
```
[1] 加藤 慎也, 天方 大地, 西尾 俊哉, 原 隆浩, "ストリーミング時系列データの効率的なモチーフモニタリングアルゴリズム," 情報処理学会マルチメディア，分散，協調とモバイル(DICOMO2018)シンポジウム論文集, pages 1473-1480 2018年7月.
```

+ Table View

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|type|book|authors|title|pub_date[0]年 pub_date[1]月|link|

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|国内会議(査読あり)|情報処理学会マルチメディア，分散，協調とモバイル(DICOMO2018)シンポジウム論文集|加藤 慎也, 天方 大地, 西尾 俊哉, 原 隆浩|ストリーミング時系列データの効率的なモチーフモニタリングアルゴリズム|2018年7月|link|


#### Domestic Conference

+ Bibtex View
```
@inproceedings{<id>,
         title = {<title_ja>or<title_en>},
        author = {<authors_ja>},
       journal = {<book>},
         month = {<pub_date[1]>},
          year = {<pub_date[0]>},
          note = {<note>},
}
```
```
@article{id911,
         title = {位置情報サービス利用におけるダミーを用いたユーザ位置曖昧化手法の視認性評価},
        author = {林田 秀平 and 天方 大地 and 原 隆浩 and Xing Xie},
       journal = {第10回データ工学と情報マネジメントに関するフォーラム（DEIMフォーラム2018）},
         month = {3},
          year = {2018},
          note = {文部科学省科学研究費補助金・基盤研究 (A)(JP26240013),挑戦的萌芽研究(JP16K12429)，開催地：芦原温泉，福井県，開催日程：3/4-3/6，発表日：3/5},
}
```

+ List View
```
[1] <authors_ja>, "<title_ja>or<title_en>," <book>,  <pub_date[0]>年<pub_date[1]>月.
```
```
[1] 林田 秀平, 天方 大地, 原 隆浩, Xing Xie, "位置情報サービス利用におけるダミーを用いたユーザ位置曖昧化手法の視認性評価," 第10回データ工学と情報マネジメントに関するフォーラム（DEIMフォーラム2018）, 2018年3月.
```

+ Table View

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|type|book|authors|title|pub_date[0]年 pub_date[1]月|link|

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|国内研究会|情報処理学会マルチメディア，分散，協調とモバイル(DICOMO2018)シンポジウム論文集|加藤 慎也, 天方 大地, 西尾 俊哉, 原 隆浩|位置情報サービス利用におけるダミーを用いたユーザ位置曖昧化手法の視認性評価|2018年7月|link|


#### National Conference

+ Bibtex View
```
@inproceedings{<id>,
         title = {<title_ja>or<title_en>},
        author = {<authors_ja>},
     booktitle = {<book>},
         month = {<pub_date[1]>},
          year = {<pub_date[0]>},
}
```
```
@inproceedings{id914,
         title = {社会センサデータ生成・共有基盤におけるストリーミングデータ処理機構},
        author = {中嶋 奎介 and 横山 正浩 and 義久 智樹 and 原 隆浩},
     booktitle = {IPSJ情報処理学会第80回全国大会},
         month = {3},
          year = {2018},
}
```

+ List View
```
[1] <authors_ja>, "<title_ja>or<title_en>," <book>,  <pub_date[0]>年<pub_date[1]>月.
```
```
[1] 中嶋 奎介, 横山 正浩, 義久 智樹, 原 隆浩, "社会センサデータ生成・共有基盤におけるストリーミングデータ処理機構," IPSJ情報処理学会第80回全国大会, 2018年3月.
```

+ Table View

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|type|book|authors|title|pub_date[0]年 pub_date[1]月|link|

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|全国大会|IPSJ情報処理学会第80回全国大会|中嶋 奎介, 横山 正浩, 義久 智樹, 原 隆浩|社会センサデータ生成・共有基盤におけるストリーミングデータ処理機構|2018年3月|link|


#### Book/Review/Editor/Translation

+ Bibtex View
```
@article{<id>,
         title = {<title_ja>or<title_en>},
        author = {<authors_ja>or<authors_en>},
     booktitle = {<book>},
         pages = {<page>},
         month = {<pub_date[1]>},
          year = {<pub_date[0]>},
}
```
```
@article{id921,
         title = {Fusion of Heterogeneous Mobile Data, Challenges and Solutions},
        author = {Takahiro Hara},
     booktitle = {Adaptive Mobile Computing: Advances in Processing Mobile Data Sets (Chapter 3), Elsevier},
         pages = {47-63},
         month = {8},
          year = {2017},
}
```

+ List View
```
[1] <authors_ja>or<authors_en>, "<title_ja>or<title_en>," <book>, pages <page> <pub_date[1]> <pub_date[0]>.
```
```
[1] Takahiro Hara, "Fusion of Heterogeneous Mobile Data, Challenges and Solutions," Adaptive Mobile Computing: Advances in Processing Mobile Data Sets (Chapter 3), Elsevier, pages 47-63 August 2017.
```

+ Table View

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|type|book|authors|title|pub_date[0]年 pub_date[1]月|link|

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|著書／監修／編集／訳書|Challenges and Solutions," Adaptive Mobile Computing: Advances in Processing Mobile Data Sets (Chapter 3)|Takahiro Hara|Fusion of Heterogeneous Mobile Data, Challenges and Solutions|2017年8月|link|


#### Presentaion/Panel Discution/Seminer

+ Bibtex View
```
@article{<id>,
         title = {<title_ja>or<title_en>},
        author = {<authors_ja>or<authors_en>},
       journal = {<book>},
         month = {<pub_date[1]>},
          year = {<pub_date[0]>},
}
```
```
@article{id2749,
         title = {実世界指向AIが引き起こすイノベーション},
        author = {前川 卓也},
       journal = {第一回ビジネスedgeセミナー「AIは経営とビジネスモデルにどんなイノベーションを起こすのか」基調講演},
         month = {6},
          year = {2018},
}
```

+ List View
```
[1] <authors_ja>or<authors_en>, "<title_ja>or<title_en>," <book>, <pub_date[0]>年<pub_date[1]>月.
```
```
[1] 前川 卓也, "実世界指向AIが引き起こすイノベーション," 第一回ビジネスedgeセミナー「AIは経営とビジネスモデルにどんなイノベーションを起こすのか」基調講演, 2018年6月.
```

+ Table View

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|type|book|authors|title|pub_date[0]年 pub_date[1]月|link|

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|基調講演/セミナー・パネル討論等|実世界指向AIが引き起こすイノベーション|前川 卓也|第一回ビジネスedgeセミナー「AIは経営とビジネスモデルにどんなイノベーションを起こすのか」基調講演|2018年6月|link|


#### News Paper article

+ Bibtex View
```
@article{<id>,
         title = {<title_ja>or<title_en>},
        author = {<authors_ja>or<authors_en>},
       journal = {<book>},
         month = {<pub_date[1]>},
          year = {<pub_date[0]>},
}
```
```
@article{id902,
         title = {世界初! AIを使った生き物目線の映像},
        author = {前川 卓也},
       journal = {MBSテレビ ちちんぷいぷい},
         month = {9},
          year = {2017},
}
```

+ List View
```
[1] <authors_ja>or<authors_en>, "<title_ja>or<title_en>," <book>, <pub_date[0]>年<pub_date[1]>月.
```
```
[1] 前川 卓也, "世界初! AIを使った生き物目線の映像," MBSテレビ ちちんぷいぷい, 2017年9月.
```

+ Table View

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|type|book|authors|title|pub_date[0]年 pub_date[1]月|link|

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|新聞報道記事|世界初! AIを使った生き物目線の映像|前川 卓也|MBSテレビ ちちんぷいぷい|2017年9月|link|


#### Others

+ Bibtex View
```
@article{<id>,
         title = {<title_ja>or<title_en>},
        author = {<authors_ja>or<authors_en>},
       journal = {<book>},
        volume = {<volume>},
        number = {<number>},
         pages = {<pages>},
         month = {<pub_date[1]>},
          year = {<pub_date[0]>},
}
```
```
@article{id965,
         title = {「デジタルコンテンツクリエーション最前線」開催報告},
        author = {義久 智樹 and 水野 慎士 and 三上 浩司 and 林 洋人 and 楠 房子},
       journal = {情報処理学会論文誌デジタルコンテンツ (DCON)},
        volume = {5},
        number = {2},
         pages = {1-1},
         month = {8},
          year = {2017},
}
```

+ List View
```
[1] <authors_ja>or<authors_en>, "<title_ja>or<title_en>," <book>, volume <volume>, number <number>, <pages> <pub_date[0]>年<pub_date[1]>月.
```
```
[1] 義久 智樹, 水野 慎士, 三上 浩司, 林 洋人, 楠 房子, "「デジタルコンテンツクリエーション最前線」開催報告," 情報処理学会論文誌デジタルコンテンツ (DCON), volume 5, number 2, 1-1 2017年8月.
```

+ Table View

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|type|book|authors|title|pub_date[0]年 pub_date[1]月|link|

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|その他（一般記事等）|「デジタルコンテンツクリエーション最前線」開催報告|義久 智樹, 水野 慎士, 三上 浩司, 林 洋人, 楠 房子|情報処理学会論文誌デジタルコンテンツ (DCON)|2017年8月|link|


#### Award

+ Bibtex View
```
@inproceedings{<id>,
         title = {<title_ja>or<title_en>},
        author = {<authors_ja>or<authors_en>},
     booktitle = {<book>},
         month = {<pub_date[1]>},
          year = {<pub_date[0]>},
}
```
```
@inproceedings{id2757,
         title = {ヤングリサーチャ賞},
        author = {神谷 俊充 and 中村 達哉 and 前川 卓也 and 天方 大地 and 原 隆浩},
     booktitle = {情報処理学会マルチメディア，分散，協調とモバイル(DICOMO2018)シンポジウム論文集},
         month = {7},
          year = {2018},
}
```

+ List View
```
[1] <authors_ja>or<authors_en>, "<title_ja>or<title_en>," <book>, <pub_date[0]>年<pub_date[1]>月.
```
```
[1] 神谷 俊充, 中村 達哉, 前川 卓也, 天方 大地, 原 隆浩, "ヤングリサーチャ賞," 情報処理学会マルチメディア，分散，協調とモバイル(DICOMO2018)シンポジウム論文集, 2018年7月.
```

+ Table View

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|type|book|authors|title|pub_date[0]年 pub_date[1]月|link|

|/|論文誌/会議名|著者名|表題|出版年月|Link|
|----|----|----|----|----|----|
|受賞|ヤングリサーチャ賞|神谷 俊充, 中村 達哉, 前川 卓也, 天方 大地, 原 隆浩|情報処理学会マルチメディア，分散，協調とモバイル(DICOMO2018)シンポジウム論文集|2018年7月|link|

-天方さんにBook/Review/...のtypeをどうするか相談！

## Search Function
Use search form.



### memo (東出)
クエリをPOSTするのか，get prameterを使うのかは要検討.
