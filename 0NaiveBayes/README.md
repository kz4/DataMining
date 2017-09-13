# Naive Bayes

## Result
```
input:
python3 solution.py data1.csv play 1 overcast 83 86 FALSE

output:
P(no;alpha=1)=0.35714285714285715
P(yes;alpha=1)=0.6428571428571429
P(humidity|no;alpha=1) = N(mean=86.2, sd=9.731392500562292)
P(humidity|yes;alpha=1) = N(mean=79.11111111111111, sd=10.215728613814635)
P(outlook=sunny|yes;alpha=1) = 0.2222222222222222
P(outlook=overcast|yes;alpha=1) = 0.4444444444444444
P(outlook=rainy|yes;alpha=1) = 0.3333333333333333
P(windy=TRUE|no;alpha=1) = 0.6
P(windy=TRUE|yes;alpha=1) = 0.3333333333333333
P(windy=FALSE|no;alpha=1) = 0.4
P(windy=FALSE|yes;alpha=1) = 0.6666666666666666
P(temp|yes;alpha=1) = N(mean=73.0, sd=6.164414002968976)
P(temp|no;alpha=1) = N(mean=74.6, sd=7.893034904268446)
P(outlook=overcast|no;alpha=1) = 0.125
P(outlook=sunny|no;alpha=1) = 0.5
P(outlook=rainy|no;alpha=1) = 0.375
Input:  ['overcast', '83', '86', 'FALSE']
P(no;alpha=1)=0.35714285714285715
P(outlook=overcast|no;alpha=1) = 0.125
P(temp=83|no;alpha=1) = 0.028689864240848583
P(humidity=86|no;alpha=1) = 0.04098673806047726
P(windy=FALSE|no;alpha=1) = 0.4
P(x|no) = 5.879519753151571e-05
P(yes;alpha=1)=0.6428571428571429
P(outlook=overcast|yes;alpha=1) = 0.4444444444444444
P(temp=83|yes;alpha=1) = 0.017361136822063646
P(humidity=86|yes;alpha=1) = 0.03110971096779443
P(windy=FALSE|yes;alpha=1) = 0.6666666666666666
P(x|yes) = 0.000160029614401995
P(x) =  0.000123874465519681

input:
python3 solution.py data2.csv sign 1 blue square

output:
P(plus;alpha=1)=0.5833333333333334
P(minus;alpha=1)=0.4166666666666667
P(color=black|plus;alpha=1) = 0.2857142857142857
P(color=black|minus;alpha=1) = 0.2
P(color=blue|plus;alpha=1) = 0.42857142857142855
P(color=blue|minus;alpha=1) = 0.6
P(color=red|plus;alpha=1) = 0.2857142857142857
P(color=red|minus;alpha=1) = 0.2
P(shape=square|plus;alpha=1) = 0.7142857142857143
P(shape=square|minus;alpha=1) = 0.6
P(shape=circle|plus;alpha=1) = 0.2857142857142857
P(shape=circle|minus;alpha=1) = 0.4
Input:  ['blue', 'square']
P(plus;alpha=1)=0.5833333333333334
P(color=blue|plus;alpha=1) = 0.42857142857142855
P(shape=square|plus;alpha=1) = 0.7142857142857143
P(x|plus) = 0.30612244897959184
P(minus;alpha=1)=0.4166666666666667
P(color=blue|minus;alpha=1) = 0.6
P(shape=square|minus;alpha=1) = 0.6
P(x|minus) = 0.36
P(x) =  0.32857142857142857

input:
python3 solution.py data2.csv sign 1 orange square

output:
P(plus;alpha=1)=0.5833333333333334
P(minus;alpha=1)=0.4166666666666667
P(shape=circle|plus;alpha=1) = 0.2857142857142857
P(shape=circle|minus;alpha=1) = 0.4
P(shape=square|plus;alpha=1) = 0.7142857142857143
P(shape=square|minus;alpha=1) = 0.6
P(color=blue|plus;alpha=1) = 0.42857142857142855
P(color=blue|minus;alpha=1) = 0.6
P(color=red|plus;alpha=1) = 0.2857142857142857
P(color=red|minus;alpha=1) = 0.2
P(color=black|plus;alpha=1) = 0.2857142857142857
P(color=black|minus;alpha=1) = 0.2
Input:  ['orange', 'square']
P(plus;alpha=1)=0.5833333333333334
P(color=orange|plus;alpha=1) = 0.09090909090909091
P(shape=square|plus;alpha=1) = 0.7142857142857143
P(x|plus) = 0.06493506493506494
P(minus;alpha=1)=0.4166666666666667
P(color=orange|minus;alpha=1) = 0.1111111111111111
P(shape=square|minus;alpha=1) = 0.6
P(x|minus) = 0.06666666666666667
P(x) =  0.06565656565656566
```

