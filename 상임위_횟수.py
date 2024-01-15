#소위원회

so_cnt_re<- so %>%
	filter(str_detect(소위원회,'법')) %>%
	mutate(which_so = str_extract(소위원회, "[ㄱ-힣]{1,}위원회"),
				 date = as_date(str_extract(소위원회, "[0-9]{4}년[0-9]{2}월[0-9]{2}일")),
				 year_d = year(date),
				 month_d = month(date)) %>%
	group_by(상임위, which_so, year_d, month_d) %>%
	summarize(cnt = n(),
						promise = ifelse(cnt>=3, 'O','X'))

#지킨 게 몇번이니
so_cnt_re %>% mutate(date_d = as_date(paste0(year_d,'-',month_d,'-01'))) %>%
	group_by(상임위, which_so) %>%
	summarize(first_d = min(date_d),
						last_d = max(date_d),
						cnt_O = length(which(promise=="O"))) %>% View()

#상임위원회
sang <- read_xlsx('국회/상임위 개회.xlsx')

sang %>% filter(str_detect(개회,"제[0-9]차")) %>% View()

sang_cnt <- sang %>% filter(str_detect(개회,"제[0-9]{1,}차")) %>%
	mutate(sang_date = as_date(str_extract(개회, "[0-9]{4}년[0-9]{2}월[0-9]{2}일")),
				 year_s = year(sang_date),
				 month_s = month(sang_date)) %>%
	filter(sang_date < as_date('2023-10-01')) %>%
	group_by(상임위, year_s, month_s) %>%
	summarize(cnt = n(),
	promise = ifelse(cnt>=2, 'O','X'))

sang_cnt %>% filter(promise=="O") %>%
  group_by(상임위) %>% summarize(cnt_O = n()) %>% View()

sang_cnt %>% filter((month_s==10)) %>%
   filter(promise=="X") %>%
   group_by(상임위) %>% summarize(cnt_O = n()) %>% View()
