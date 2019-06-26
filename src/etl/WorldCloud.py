import pickle
from os import path
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
def make_worldcloud(file_path):
    text_from_file_with_apath = open(file_path,'r',encoding='UTF-8').read()
    wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=False)
    wl_space_split = " ".join(wordlist_after_jieba)
    print(wl_space_split)
    backgroud_Image = plt.imread('test.png')
    print('加载图片成功！')
    '''设置词云样式'''
    stopwords = STOPWORDS.copy()
    stopwords.add("哈哈") #可以加多个屏蔽词
    wc = WordCloud(
        width=1024,
        height=768,
        background_color='white',# 设置背景颜色
        mask=backgroud_Image,# 设置背景图片
        font_path='simsun.ttf',  # 设置中文字体，若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
        max_words=600, # 设置最大现实的字数
        stopwords=stopwords,# 设置停用词
        max_font_size=400,# 设置字体最大值
        random_state=50,# 设置有多少种随机生成状态，即有多少种配色方案
    )
    wc.generate_from_text(wl_space_split)#开始加载文本
    img_colors = ImageColorGenerator(backgroud_Image)
    wc.recolor(color_func=img_colors)#字体颜色为背景图片的颜色
    plt.imshow(wc)# 显示词云图
    plt.axis('off')# 是否显示x轴、y轴下标
    plt.show()#显示
    # 获得模块所在的路径的
    d = path.dirname(__file__)
    # os.path.join()：  将多个路径组合后返回
    wc.to_file(path.join(d, "h11.jpg"))
    print('生成词云成功!')

make_worldcloud('test-data.txt')

# from wordcloud import WordCloud

# f = open(u'test-data.txt','r', encoding='gbk', errors='ignore').read()
# wordcloud = WordCloud(background_color="white",width=1000, height=860, margin=2).generate(f)

# # width,height,margin可以设置图片属性

# # generate 可以对全部文本进行自动分词,但是他对中文支持不好,对中文的分词处理请看我的下一篇文章
# #wordcloud = WordCloud(font_path = r'D:\Fonts\simkai.ttf').generate(f)
# # 你可以通过font_path参数来设置字体集

# #background_color参数为设置背景颜色,默认颜色为黑色

# import matplotlib.pyplot as plt
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()

# wordcloud.to_file('test.png')
# # 保存图片,但是在第三模块的例子中 图片大小将会按照 mask 保存