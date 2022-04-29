library(plyr)
library(ggplot2)
library(rstudioapi)

###Set working directory to source file location.
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

###Read in data for fam36415.
data <- read.delim("syas_summary.csv")

###Drop data with IDs that equal 0.
data <- data[!(data$Indiv1 == '0' | data$Indiv2 == '0'),]
data <- na.omit(data)

###Limit frequencies to only 0 GD relationships.
mydata <- data[data$generation.depth == '0', ]

###Concatenate GD and ME into one column for frequency counts.
mydata$relation <- paste(mydata$relationship.type,",", mydata$generation.depth, ",", mydata$meioses.events)

###Create frequency data frame.
sel_col <- c('Indiv1', 'relation')
frequency <- count(mydata, sel_col)

###Rename columns
names(frequency)[3] <- 'Frequencies'
names(frequency)[2] <- 'Relationship_Type'

###Create violin plot.
vp <- ggplot(frequency, aes(x=factor(Relationship_Type), y=Frequencies)) +
               geom_violin() +
  scale_x_discrete(name ='Relationship', labels=c('Full Siblings','Full 1st Cousins', 'Full 2nd Cousins', 
  'Half Siblings', 'Half 1st Cousins', 'Half 2nd Cousins', 'Unknown Siblings', 'Unknown 1st Cousins')) +
  theme_bw()
vp