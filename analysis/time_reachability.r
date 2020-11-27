# Time Reachability
#--------------------------------------------------------------------------------------------------
fmt <- function(){ #formatting 3 decimals precision
  f <- function(x) as.character(round(x,3))
  f
}
library(ggplot2)
x <- c(10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140)
y <- c(100,155,199,231,257,289,315,334,360,391,413,448,484,521)
h <- c(8,9,12,14,19,12,12,14,13,15,16,17,19,26)
reach_plot <- qplot(x, y, xlab = "Número de Dispositivos", ylab = "Tempo de Execução (ms)") +
  geom_line(col = "blue") +
  theme(text = element_text(size=14),
        axis.text.x = element_text(angle=0, hjust=1)) +
  geom_errorbar (aes(ymin=y-h, ymax=y+h), width=1, position=position_dodge((.9))) +
  scale_x_continuous (breaks = x) +
  scale_y_continuous (breaks = y, labels = fmt()) 
  #coord_trans(x = "log10")# + geom_errorbar(limits, position="dodge", width=0.25)
reach_plot
