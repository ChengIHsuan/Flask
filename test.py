class test():
    def ifnull(self, aaa):
        str1 = ''
        str2 = ''
        for a in aaa:
            str1 += 'ifnull({}, 0) + '.format(a)
            str2 += 'count({}) + '.format(a)
        str1 = '('+str1[:-3]+')'
        str2 = '(' + str2[:-3] + ')'
        print(str1 + ' / ' + str2 + ', ')
    def avg(self):
        str = ''
        for a in range(9):
            str += 'avg(v_10{}) as v_10{}, '.format(a+1, a+1)
        for b in range(10, 34):
            str += 'avg(v_1{}) as v_1{}, '.format(b, b)
        print(str)

# test().ifnull(['v_106', 'v_113', 'v_114', 'v_117', 'v_118', 'v_120', 'v_124', 'v_125'])
# test().ifnull(['v_115', 'v_121', 'v_122', 'v_123', 'v_131'])
# test().ifnull(['v_103', 'v_105', 'v_107'])
# test().ifnull([ 'v_108', 'v_119', 'v_132',])
# test().ifnull([ 'v_109', 'v_110', 'v_111', 'v_112', 'v_116',])
# test().ifnull([ 'v_126', 'v_128', 'v_133',])
test().avg()

