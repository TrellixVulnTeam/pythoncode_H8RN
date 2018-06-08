#encoding=utf-8

# Copyright (c) 2017 Deyatech. All rights reserved.
# Authors: Peter Podstreleny <peter.podstreleny@deyatech.com>

# pre-process-target.py

# This script loads target .txt document specified in 'import_path' and it runs
# following steps on the content of the file:

# 1.) Segment text into words
# 2.) Remove all whitespace characters
# 3.) Remove all punctuation characters
# 4.) Remove initial python unicode character (\ufeff)
# 5.) Remove all numbers
# 6.) Remove all percentage numbers
# 7.) Remove all ordering and bulleting characters
# 8.) Remove specified stopwords
# 9.) Remove all repeating characters ('___', 'xxx', '...', '###')
# 10.) Save all words (English) into lowercase

# The processed file is saved in specified 'export_path'.

import os
import json
import jieba

user = 'admin'

labels = [
    { 'label': 'target',
      'import_path': 'c:/Users/' + user + '/Dropbox/AI Project/AI/bin/target/input/',
      'export_path': 'c:/Users/' + user + '/Dropbox/AI Project/AI/bin/target/output/' }
]

punctuation_string = (". “ ” ( ) _ : - / , ： （ ） 《 》 ， 、 。 ； % ? ？ ! ！")
ordering_string = ("a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D "
                   "E F G H I J K L M N O P Q R S T U V W X Y Z i ii iii iv v "
                   "vi vii viii ix x xi xii xiii xiv xv xvi xvii xviii xix xx "
                   "〇 一 二 三 四 五 六 七 八 九 零 ")
others_string = ("@ 【 】 * ￥ ·  & | + ％ [ ] × ～ ． ① ② ③ — －    ┃ © ﹪ "
                 "® = ' \ \" – ~ < > ; ■ { } # #. • ｜ …  ‘ ’ ⅱ  ⬆ ⬇  ... ⋯ "
                 "◆ √   □  ...... ― 「 」 『 』 ／ ④ ⑤ ⑥  $ ⅱ xxx")
# https://www.ranks.nl/stopwords/chinese-stopwords
stopwords_string = ("的 一 不 在 人 有 是 为 以 于 上 他 而 后 之 来 及 了 因 下 可 "
                    "到 由 这 与 也 此 但 并 个 其 已 无 小 我 们 起 最 再 今 去 好 "
                    "只 又 或 很 亦 某 把 那 你 乃 它 吧 被 比 别 趁 当 从 到 得 打 "
                    "凡 儿 尔 该 各 给 跟 和 何 还 即 几 既 看 据 距 靠 啦 了 另 么 "
                    "每 们 嘛 拿 哪 那 您 凭 且 却 让 仍 啥 如 若 使 谁 虽 随 同 所 "
                    "她 哇 嗡 往 哪 些 向 沿 哟 用 于 咱 则 怎 曾 至 致 着 诸 自")


def isNumber(s):
    if 'inf' == s.lower():
        return False
    else:
        try:
            int(float(s))
            return True
        except ValueError:
            return False

def isUnderline(s):
    if (s[0] == '_') and (len(set(s)) == 1):
        return True
    else:
        return False

def isDots(s):
    if (s[0] == '.') and (len(set(s)) == 1):
        return True
    else:
        return False

def isX(s):
    if (s[0] == 'x') and (len(set(s)) == 1):
        return True
    else:
        return False

def isHash(s):
    if (s[0] == '#') and (len(set(s)) == 1):
        return True
    else:
        return False

def isPercentageNumber(string):
    if '%' in string:
        try:
            int(float(string.split('%')[0]))
            return True
        except ValueError:
            return False
    else:
        return False

print('-------------------------------------------------------------------')
print('--- Pre-processing target data')
print('-------------------------------------------------------------------')

for label in labels:
    print('--- Pre-processing ' + label['label'] + ' data ...')

    for filename in os.listdir(label['import_path']):
        print('-------------------------------------------------------------------')
        print('--- File: ' + filename)
        print('... opening ...')
        with open(label['import_path'] + filename, 'r', encoding="utf8") as f1:
            content = f1.read()

        # Segment content
        content = jieba.cut(content, cut_all=False)  # 'cut_all=False' is parameter that runs 'Accurate' segmentation mode
        print('... segmenting ...')
        # Strip any whitespace characters
        content = [x.strip() for x in content]
        print('... stripping whitespace characters ...')
        # Remove any punctuation characters
        content = [x for x in content if x not in punctuation_string]
        print('... removing punctuation characters ...')
        # Remove initial file unicode character
        content = [x for x in content if x != '\ufeff']
        print('... removing initial unicode character (\\ufeff) ...')
        # Remove any numbers
        content = [x for x in content if isNumber(x) != True]
        print('... removing numbers ...')
        # Remove any percentage numbers
        content = [x for x in content if isPercentageNumber(x) != True]
        print('... removing percentage numbers ...')
        # Remove any ordering string
        content = [x for x in content if x not in ordering_string]
        print('... removing ordering and bulletpoint characters ...')
        # Remove other not needed characters
        content = [x for x in content if x not in others_string]
        print('... removing other not needed characters ...')
        # Remove stopwords
        content = [x for x in content if x not in stopwords_string]
        print('... removing stopwords ...')
        # Remove '_____'
        content = [x for x in content if isUnderline(x) != True]
        print('... removing underline ...')
        # Remove 'xxxx'
        content = [x for x in content if isX(x) != True]
        print('... remove xxx ...')
        # Remove '#####'
        content = [x for x in content if isHash(x) != True]
        print('... remove ### ...')
        # Remove '...'
        content = [x for x in content if isDots(x) != True]
        print('... remove ... ...')
        # Transfer all to lowercase
        content = [x.lower() for x in content]

        print('... saving ...')

        document = {'label': label['label'], 'body': content}

        with open(label['export_path'] + filename, 'w', encoding='utf8') as f2:
             f2.write(json.dumps(document))

        # The below code lists down all words in human readable form, so it
        # is easy to identify if there are any other characters that should be
        # cleaned and removed.

        # with open(label['export_path'] + filename.split('.')[0] + '-readable.txt', 'w', encoding='utf8') as f3:
        #     for item in content:
        #         f3.write(item + os.linesep)
