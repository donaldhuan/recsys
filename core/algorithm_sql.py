import sqlite3
conn = sqlite3.Connection('/Users/aegiryy/Projects/recsys/recsys.sqlite3')
DEBUG = True 

def sim(u, v):
    I = corate(u, v)
    Ru = averate(u, I)
    Rv = averate(v, I)
    a = 0
    b = 0
    c = 0
    cu = conn.execute('select movie_id, rating from core_rating where user_id = %d and movie_id in %s' % (u, _genstr(I)))
    rsu = cu.fetchall()
    rsu.sort()
    cv = conn.execute('select movie_id, rating from core_rating where user_id = %d and movie_id in %s' % (v, _genstr(I)))
    rsv = cv.fetchall()
    rsv.sort()
    for i in range(0, len(rsu)):
        a += (rsu[i][1] - Ru) * (rsv[i][1] - Rv)
        b += (rsu[i][1] - Ru) ** 2
        c += (rsv[i][1] - Rv) ** 2
    from math import sqrt
    if b * c == 0:
        return 0
    return a / sqrt(b * c)

def corate(u, v):
    c = conn.execute('select movie_id from core_rating where user_id = %d and movie_id in (select movie_id from core_rating where user_id = %d)' % (u, v))
    return [k[0] for k in c]

def averate(u, I = None):
    if I is None:
        return conn.execute('select avg(rating) from core_rating where user_id = %d' % u).fetchone()[0]
    try:
        return conn.execute('select avg(rating) from core_rating where user_id = %d and movie_id in %s' % (u, _genstr(I))).fetchone()[0]
    except:
        print u
        print I
        print _genstr(I)

def guess(u, i):
    P = 0
    Ru = averate(u)
    a = 0
    b = 0
    # vs = [k[0] for k in conn.execute('select user_id from core_rating where movie_id = %d' % i).fetchall()]
    # cursor = conn.execute('select user_id, rating from core_rating where movie_id = %d and user_id in %s' % (i, _genstr(vs)))
    cursor = conn.execute('select user_id, rating from core_rating where movie_id = %d' % i)
    rs = cursor.fetchall()
    for c in range(0, len(rs)):
        if DEBUG:
            print '%d / %d' % (c, len(rs))
        if u != rs[c][0]:
            # s = sim(u, rs[c][0])
            s = conn.execute('select similarity from core_similarity where id = %d' % (u * 1000 + rs[c][0])).fetchone()[0]
            a += s * (rs[c][1] - averate(rs[c][0]))
            b += abs(s)
    try:
        return a * 1.0 / b + Ru
    except:
        # exception occurs only when no other users rated this item
        return None

def _genstr(lst):
    '''lst  [1, 2, 3]
    return  '(1, 2, 3)'
    '''
    buf = ['(']
    buf.append(str(lst)[1:-1])
    buf.append(')')
    return ''.join(buf)

if __name__ == '__main__':
    from sys import exit
    from datetime import datetime
    t = datetime.now()
    print guess(7, 599)
    print datetime.now() - t
    exit(0)
    # from datetime import datetime
    # t = datetime.now()
    USER_ID = 1
    for USER_ID in range(7, 944):
        rs = conn.execute('select movie_id, rating from core_rating where user_id = %d' % USER_ID).fetchall()
        result = []
        cnt = 0
        for e in rs:
            result.append(e[1] - guess(USER_ID, e[0]))
            print '%d/%d' % (cnt, len(rs))
            cnt += 1
        f = open('result/result_%d' % USER_ID, 'w')
        import pickle
        pickle.dump(result, f)
        f.flush()
        f.close()
    # print datetime.now() - t
