setwd("C:\\Users\\dsharp\\Documents\\Udacity\\Udacity\\EDA")

reddit <- read.csv('reddit.csv')
table(reddit$employment.status)
summary(reddit)
reddit$age.range <- ordered(reddit$age.range, levels = c("Under 18","18-24","25-34","35-44","45-54","55-64","65 or Above"))
       
       
#<- c(1, 2, 3, 4, 5, 6, 0)
factor(c(1, 2, 3, 4, 5, 6, 0), labels=levels(reddit$age.range))

ordered(reddit, levels = c("18-24","25-34","35-44","45-54","55-64","65 or Above","Under 18"))
library(ggplot2)
qplot(data = reddit, x = age.range)
plot(reddit$age.range)
