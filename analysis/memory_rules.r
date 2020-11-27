# Memory Rules
#--------------------------------------------------------------------------------------------------
fmt <- function(){ #formatting 3 decimals precision
  f <- function(x) as.character(round(x,3))
  f
}
library(ggplot2)
x <- c(1500, 3000, 4500, 6000, 7500, 9000, 10500, 12000, 13500, 15000, 16500, 18000)
y <- c(12.06, 13.45, 14.69, 16.56, 18.48, 21.48, 23.80, 26.92, 31.16, 37.18, 44.99, 54.45) # this is the mean value runtime
h <- c(0.6,0.7,1,1.4,1.1,1.0,1.0,1.1,1.2,1.5,1.5,1.9)
reach_plot <- qplot(x, y, xlab = "Número de Fluxos", ylab = "Memória Utilizada (MB)") +
  geom_line(col = "blue") +
  theme(text = element_text(size=14),
        axis.text.x = element_text(angle=0, hjust=1)) +
  geom_errorbar (aes(ymin=y-h, ymax=y+h), width=1, position=position_dodge((.9))) +
  scale_x_continuous (breaks = x) +
  scale_y_continuous (breaks = y, labels = fmt())
  #coord_trans(x = "log10")# + geom_errorbar(limits, position="dodge", width=0.25)
reach_plot
