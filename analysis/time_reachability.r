# Time Reachability
#--------------------------------------------------------------------------------------------------
fmt <- function(){ #formatting 3 decimals precision
  f <- function(x) as.character(round(x,3))
  f
}
library(ggplot2)
x <- c(1284, 2274, 3109, 4779, 5743, 6193, 7123, 8129, 9190, 10610, 12115, 13615, 14812, 16013)
y <- c(1.39,  2.3, 3.05, 4.71, 5.57, 5.99, 6.72, 7.28, 7.43, 7.80, 8.13, 8.28, 8.44, 8.61) # this is the mean value runtime
reach_plot <- qplot(x, y, xlab = "Número de Fluxos", ylab = "Tempo de Execução (s)") +
  geom_line(col = "blue") +
  scale_x_continuous (breaks = x) +
  scale_y_continuous (breaks = y, labels = fmt()) +
  coord_trans(x = "log10") #+ geom_errorbar(limits, position="dodge", width=0.25)
reach_plot


