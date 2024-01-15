Sys.setlocale(category = "LC_CTYPE", locale = "ko_KR.UTF-8")

library(pscl)
library(wnominate)
library(foreign)
library(gdata)
library(magrittr)
library(dplyr)
library(gridExtra)
library(ggrepel)
library(ggplot2)
library(extrafont)
library(svglite)

# 국회의원별로 찬성 1, 반대 2, 기권 3, 참석안함 4로 만든 데이터프레임 가져오기
pg<- read.csv("/Users/mabuintern/Desktop/mabujakchim/국회일했나/wnominate/wnominate_전체.csv",header=TRUE,strip.white=TRUE)
pg<- pg[-1,]

#정당 붙여주기
uiwon_df <- read.csv('/Users/mabuintern/Desktop/21대국회/data/국회의원명단_장관_사임_포함_1107.csv', encoding='utf-8')

uiwonparty<- uiwon_df[,c('의원명','정당','uniquenum')]
uiwonparty<- uiwonparty %>% rename("uiwon" = "uniquenum", "party" = "정당")

pg<- pg %>% rename("uiwon" = "X")

#merge
pg<- merge(pg, uiwonparty, by='uiwon')
pg<- pg %>% relocate(c('의원명','uiwon','party'))

legData<- matrix(pg[,3], length(pg[,3]),1)
colnames(legData)<- "party"

pgnames<- pg[,2]
pgnames<- as.character(pgnames)
pg <- pg[,-c(1,2,3)]

# uiwon rc
rc <- rollcall(pg,
                yea=1,
                nay=2,
               missing=3,
               notInLegis=4,
	       legis.names=pgnames,
               legis.data=legData)

#  Call W-NOMINATE
#  Run wnominate on rollcall object
# polarity는 국힘 원내대표 국회의원의 index number로 설정
pg_result <- wnominate(rc, dims=2, polarity=c(31,31))

par(family='AppleGothic')
summary(pg_result)
plot(pg_result)

#dim 1
pg_result1 <- wnominate(rc, dims=1, polarity=31)
summary(pg_result)
plot(pg_result)

# 이념성향 점수 파일로 저장하기
pg_result_legis<- pg_result$legislators
pg_result1_legis<-pg_result1$legislators
write.csv(pg_result_legis, '/Users/mabuintern/Desktop/mabujakchim/국회일했나/wnominate/wnominate_2d_result_전체.csv', row.names=TRUE,fileEncoding = 'cp949')
write.csv(pg_result1_legis, '/Users/mabuintern/Desktop/mabujakchim/국회일했나/wnominate/wnominate_1d_result_전체.csv', row.names=TRUE,fileEncoding = 'cp949')


# 의원 이름 labeling
WEIGHT=(pg_result$weights[2])/(pg_result$weights[1])
X1 <- pg_result$legislators[,8]
X2 <- (pg_result$legislators[,9])*WEIGHT


uiwonparty<- uiwonparty[c(order(uiwonparty$uiwon)),]
X3<- data.frame(cbind(X1, X2))
uiwonparty<- uiwonparty[!is.na(uiwonparty$uiwon),]
X4<- data.frame(cbind(X3, uiwonparty))

theme_set(theme_minimal(base_family='AppleGothic'))

X_sub<- subset(X4, )
options(ggrepel.max.overlaps = 15)

ggplot(data=X4, aes(X1, X2, colour=party))+
  geom_text_repel(aes(X1, X2,label=의원명),point.size=3, size=3, family='NanumGothic')+
  theme_classic(base_family = "NanumGothic")+  geom_point(size=2)+
  theme(axis.text.x=element_blank())+  theme(axis.text.y=element_blank())+
  theme(axis.ticks.x=element_blank())+  theme(axis.ticks.y=element_blank())+
  ggtitle('21대 국회의원 이념 성향')+  theme(plot.title=element_text(size=20, hjust=0.5, face="bold"))+
  scale_colour_manual(values=c('#E61E2B', "#00D2C3", "#004EA2", "lawngreen", "#004A7F", "#FFED00", "#D6001C"))+
  labs(x="1D", y="2D",colour="정당")
