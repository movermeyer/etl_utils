# -*- coding: utf-8 -*-

"""
copied from https://github.com/oldhu/micolog-oldhu/blob/master/app/gbtools.py

汉字处理的工具:
判断unicode是否是汉字，数字，英文，或者其他字符。
全角符号转半角符号。

"""

__author__="internetsweeper <zhengbin0713@gmail.com>"
__date__="2007-08-04"

def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        return uchar >= u'\u4e00' and uchar<=u'\u9fa5'

def is_number(uchar):
        """判断一个unicode是否是数字"""
        return uchar >= u'\u0030' and uchar<=u'\u0039'

def is_alphabet(uchar):
        """判断一个unicode是否是英文字母"""
        return (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a')

def is_other(uchar):
        """判断是否非汉字，数字和英文字符"""
        return not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar))

def B2Q(uchar):
        """半角转全角"""
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
                return uchar
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
                inside_code=0x3000
        else:
                inside_code+=0xfee0
        return unichr(inside_code)

def Q2B(uchar):
        """全角转半角"""
        inside_code=ord(uchar)
        if inside_code==0x3000:
                inside_code=0x0020
        else:
                inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
                return uchar
        return unichr(inside_code)

def stringQ2B(ustring, convert_strs={
                                      unicode("…", "UTF-8") : u"...",
                                      u"′"                  : u"'",
                                     }):
        """把字符串全角转半角"""
        result = [Q2B(uchar) for uchar in ustring]
        result = [(((uchar in convert_strs) and convert_strs[uchar]) or uchar) for uchar in result]
        return "".join(result)

def uniform(ustring):
        """格式化字符串，完成全角转半角，大写转小写的工作"""
        return stringQ2B(ustring).lower()

def string2List(ustring):
        """将ustring按照中文，字母，数字分开"""
        retList=[]
        utmp=[]
        for uchar in ustring:
                if is_other(uchar):
                        if len(utmp)==0:
                                continue
                        else:
                                retList.append("".join(utmp))
                                utmp=[]
                else:
                        utmp.append(uchar)
        if len(utmp)!=0:
                retList.append("".join(utmp))
        return retList

if __name__=="__main__":
        assert is_chinese(u"你")
        assert not is_chinese(u"h")

        assert is_number(u"3")
        assert not is_number(u"a")

        assert is_alphabet(u"h")
        assert not is_alphabet(u"3")

        assert is_other(u"。")
        assert not is_other(u"a")

        #test Q2B and B2Q
        for i in range(0x0020,0x007F):
                print Q2B(B2Q(unichr(i))),B2Q(unichr(i))

        #test uniform
        ustring=u'中国 人名ａ高频Ａ'
        ustring=uniform(ustring)
        ret=string2List(ustring)
        print ret

        assert u"@"     == stringQ2B(u"＠")
        assert u"Z"     == Q2B(u"Ｚ")
        assert u"..."   == stringQ2B(unicode("…", "UTF-8"))
        assert u"'"     == stringQ2B(u"′")
