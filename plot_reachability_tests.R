# Ploting Reachability Formal Verification
#--------------------------------------------------------------------------------------------------

fmt <- function(){ #formatting 3 decimals precision
  f <- function(x) as.character(round(x,3))
  f
}
library(ggplot2)
x <- c(1284, 2274, 3109, 4779, 5743, 6193)
y <- c(1.39925789833,  2.3036646843, 3.05743093491, 4.71151809692, 5.57214031219, 5.99061393738) # this is the mean value runtime

reach_plot <- qplot(x, y, xlab = "Número de Fluxos", ylab = "Tempo de Execução (s)") +
  geom_line(col = "red") +
  scale_x_continuous (breaks = x) +
  scale_y_continuous (breaks = y, labels = fmt()) +
  coord_trans(x = "log10") #+ geom_errorbar(limits, position="dodge", width=0.25)

reach_plot