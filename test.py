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

test().ifnull(['v_106', 'v_113', 'v_114', 'v_117', 'v_118', 'v_120', 'v_124', 'v_125'])
test().ifnull(['v_115', 'v_121', 'v_122', 'v_123', 'v_131'])
test().ifnull(['v_103', 'v_105', 'v_107'])
test().ifnull([ 'v_108', 'v_119', 'v_132',])
test().ifnull([ 'v_109', 'v_110', 'v_111', 'v_112', 'v_116',])
test().ifnull([ 'v_126', 'v_128', 'v_133',])

