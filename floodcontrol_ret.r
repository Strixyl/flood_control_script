library(httr)
library(jsonlite)
library(dplyr)
library(openxlsx)


url <- "https://sumbongsapangulo.ph/wp-admin/admin-ajax.php"


payload <- list(
  action = "load_more",  
  page = 1
)

headers <- c(
  `X-Requested-With` = "XMLHttpRequest"
)

all_data <- list()


for (p in 1:50) {  
  payload$page <- p
  
  res <- POST(url, body = payload, encode = "form", add_headers(.headers = headers))
  

  json_res <- content(res, as = "text", encoding = "UTF-8")
  data <- fromJSON(json_res, flatten = TRUE)
  
  if (length(data$data) == 0) {
    message("No more data at page ", p)
    break
  }
  

  all_data[[p]] <- data$data
  message("Fetched page ", p)
}

df <- bind_rows(all_data)

write.csv(df, "sumbong_data.csv", row.names = FALSE)

write.xlsx(df, "sumbong_data.xlsx")
