import re
from beadsvec import BeadsVec
from dicordnum import DicOrdNum


class CyberVec:
    """Cyber Vector Notation"""

    # めんどくさいので .upper() して 'O' と数字で構成されていればOkとする
    # 辞書順記数法に対応するために、めんどくさいので '_', 'A' が含まれていてもOkとする
    __pattern1 = re.compile(r"^([_AO\d]*)$")

    @staticmethod
    def trail_zero(value=0):
        """With trailing zero"""

        element_list = None

        try:
            # 整数かどうか判定
            int_value = int(str(value), 10)

        except ValueError:
            # 整数ではなかった
            #
            # タプル型なら
            if type(value) is tuple:
                # いったんリストに戻す
                element_list = list(value)

            else:
                # TODO 整数ではなかった

                # 文字列を解析する
                element_list = CyberVec.convert_str_to_list(value)

        else:
            # 整数だ
            # リストに変換する
            element_list = []
            element_list.append(int_value)

        # 0 の要素を追加
        element_list.append(0)

        # タプルに変換して使う
        return CyberVec(tuple(element_list))

    @staticmethod
    def convert_str_to_list(text):
        # 大文字に変換
        text = text.upper()

        # '_', 'A', 'O' と数字で構成されている必要がある
        result = CyberVec.__pattern1.match(text)
        if result:
            pass
        else:
            raise ValueError(f"not cyber vector: {text}")

        # 先頭に O が付いているのは構わないものとし、
        # 先頭に付いている O は削除する
        text = text.lstrip('O')

        new_element_list = []

        # 区切り文字 O で分割
        tokens = text.split('O')

        for token in tokens:
            if token[:1] == 'A':
                # A を除去する
                n = int(token.replace('A', ''))
                new_element_list.append(n)

            elif token[:1] == '_':
                # まず '_' を除去する
                token = token.replace('_', '')

                figure = len(token)
                modulo = 1
                for i in range(0, figure):
                    modulo *= 10

                z = -1 * (modulo - int(token))
                new_element_list.append(z)

            else:
                n = int(token)
                new_element_list.append(n)

        return new_element_list

    def __init__(self, value=0, order=1):
        self._order = order

        try:
            # 整数かどうか判定
            int_value = int(str(value), 10)

        except ValueError:
            # 整数ではなかった
            #
            # タプル型なら
            if type(value) is tuple:
                # そのまま渡す
                self._beadsvec = BeadsVec(value)

            else:
                # 整数ではなかった

                # 文字列として解析する
                element_list = CyberVec.convert_str_to_list(value)
                # タプルに変換して渡す
                self._beadsvec = BeadsVec(tuple(element_list))

        else:
            # 整数だ
            # そのまま渡す
            self._beadsvec = BeadsVec(int_value)

    def __str__(self):
        """辞書順記数法 と 数珠玉記数法 の併用"""
        text = ""
        for token in self.elements:
            text = f"{text}o{DicOrdNum(token)}"

        # 先頭だけを大文字の 'O' にする
        text = f"O{text[1:]}"
        return text

    @property
    def elements(self):
        return self._beadsvec.elements
