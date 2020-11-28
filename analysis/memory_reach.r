# Memory Reachability
#--------------------------------------------------------------------------------------------------
fmt <- function(){ #formatting 3 decimals precision
  f <- function(x) as.character(round(x,3))
  f
}
library(ggplot2)
x <- c(10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140)
y <- c(10.36, 11.32, 11.86, 12.45, 13.47, 14.04, 15.42, 15.94, 16.8, 17.42, 18.15, 19.1, 20.42, 21.55)
h <- c(0.43,0.52,0.59,0.44,0.61,0.62,0.45,0.47,0.53,0.48,0.48,0.74,0.65,0.8)
reach_plot <- qplot(x, y, xlab = "Número de Dispositivos", ylab = "Memória Utilizada (MB)") +
  geom_line(col = "blue") +
  theme(text = element_text(size=14),
        axis.text.x = element_text(angle=0, hjust=1)) +
  geom_errorbar (aes(ymin=y-h, ymax=y+h), width=1, position=position_dodge((.9))) +
  scale_x_continuous (breaks = x) +
  scale_y_continuous (breaks = y, labels = fmt()) 
#coord_trans(x = "log10")# + geom_errorbar(limits, position="dodge", width=0.25)
reach_plot

