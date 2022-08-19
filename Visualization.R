library(dplyr)
library(tidyverse)
library(ggplot2)
library(rstudioapi)
library(beeswarm)

###Set working directory to source file location.
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

###Read in data.
data <- read.delim("fam36415_results.csv")
data2 <- read.delim('familinx_summary.csv')

###Limit frequencies to only 0 GD relationships.
mydata <- data[data$generation.depth == '0', ]

###Concatenate GD and ME into one column for frequency counts.
mydata$relation <- paste(mydata$relationship.type,",", mydata$generation.depth, ",", mydata$meioses.events)

###Re-encode data in order to count 0 frequencies and visualize.
mydata_f <- mydata %>% modify_if(is.character, as.factor)

tally <- mydata_f %>%
  group_by(Indiv1, relation, .drop = FALSE) %>%
  tally()

beeswarm(tally$n ~ tally$relation,
         col = c("#3FA0FF", "#6B8E23", "#F76D5E", '#AB82FF', '#00FFFF',
                 '#BF3EFF', '#FF7F24', '#424242'),
         spacing = 0.3,
         pch = 20,
         method = 'center',
         corral = 'wrap',
         labels = c('Full Sibling',
                    'Full 1st Cousin',
                    'Full 2nd Cousin',
                    'Half Sibling',
                    'Half 1st Cousin',
                    'Half 2nd Cousin',
                    'Unknown Sibling',
                    'Unknown 1st Cousin'),
         xlab = 'Relationship Type',
         ylab = 'Number of Relations per Individual')

# first_degree_relations <- subset(tally, relation == 'full , 0 , 2' | relation == 'full , 0 , 4',
#                                  select = c(relation, n))

# composite_data <- first_degree_relations %>%
#   composite(variables = c("relation", "n"), 
#             name = "Score_comp",
#             type = "sum",
#             standardize = FALSE,
#             missing.allowed = 0)

#write.csv(first_degree_relations,'first_degree_relations.csv', row.names = FALSE)

# mydata_f %>%
#   group_by(Indiv1, relation, .drop = FALSE) %>%
#   summarize(freq = n()) %>%
#   ggplot(aes(x = relation,
#              y = freq)) +
#   scale_x_discrete(name ='Relationship',
#                    labels = c('Full Sib',
#                               'Full 1 Cuz',
#                               'Full 2 Cuz',
#                               'Half Sib',
#                               'Half 1 Cuz',
#                               'Half 2 Cuz',
#                               'Unk Sib',
#                               'Unk 1 Cuz')) +
#   geom_violin() +
#   theme_bw()

#ggsave("syas_violin.png")

# ###Create frequency data frame.
# sel_col <- c('Indiv1', 'relation')
# frequency <- count(mydata_f, sel_col)
# 
# ###Rename columns
# names(frequency)[3] <- 'Frequencies'
# names(frequency)[2] <- 'Relationship_Type'

# ###Create violin plot.
# vp <- ggplot(frequency, aes(x=factor(Relationship_Type), y=Frequencies)) +
#                geom_violin() +
#   scale_x_discrete(name ='Relationship', labels=c('Full Siblings','Full 1st Cousins', 'Full 2nd Cousins', 
#   'Half Siblings', 'Half 1st Cousins', 'Half 2nd Cousins', 'Unknown Siblings', 'Unknown 1st Cousins')) +
#   theme_bw()
# vp