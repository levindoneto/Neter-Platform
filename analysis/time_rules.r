# Time Rules
#--------------------------------------------------------------------------------------------------
fmt <- function(){ #formatting 3 decimals precision
  f <- function(x) as.character(round(x,3))
  f
}
library(ggplot2)
x <- c(1500, 3000, 4500, 6000, 7500, 9000, 10500, 12000, 13500, 15000, 16500, 18000)
y <- c(0.36, 1.62, 2.85, 4.45, 6.48, 8.89, 11.92, 15.45, 17.9, 22.92, 27.15, 36.10)
h <- c(0.19,0.2,0.4,0.6,0.8,0.9,1.05,1.2,1.4,1.9,1.95,2.1)
reach_plot <- qplot(x, y, xlab = "Número de Fluxos", ylab = "Tempo de Execução (s)") +
  geom_line(col = "blue") +
  theme(text = element_text(size=14),
        axis.text.x = element_text(angle=0, hjust=1)) +
  geom_errorbar (aes(ymin=y-h, ymax=y+h), width=1, position=position_dodge((.9))) +
  scale_x_continuous (breaks = x) +
  scale_y_continuous (breaks = y, labels = fmt())
  #coord_trans(x = "log10")# + geom_errorbar(limits, position="dodge", width=0.25)
reach_plot
