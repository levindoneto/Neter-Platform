# Memory Rules
#--------------------------------------------------------------------------------------------------
fmt <- function(){ #formatting 3 decimals precision
  f <- function(x) as.character(round(x,3))
  f
}
library(ggplot2)
x <- c(540, 2274, 3109, 5193, 7123, 8129, 12115, 14812, 16013)
y <- c(12.06, 16.85, 19.09, 22.16, 24.48, 25.98, 26.80, 27.92, 29.15) # this is the mean value runtime
reach_plot <- qplot(x, y, xlab = "Número de Fluxos", ylab = "Memória Utilizada (MB)") +
  geom_line(col = "blue") +
  scale_x_continuous (breaks = x) +
  scale_y_continuous (breaks = y, labels = fmt()) 
  #coord_trans(x = "log10")# + geom_errorbar(limits, position="dodge", width=0.25)
reach_plot
