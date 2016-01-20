##This function calculates the number of groups that are associated
####### with different combinations of technology##########################################


#grpcnt is a data frame where the rows are groups and the column values are set to 1 
#if the group matches certain keywords related to the technology the column represents
#We want a matrix that represents the crosstab of each technology on each technology

grpcnt<-data1[,c("dd", "make", "rapi", "iot","vr","gp","sf","dvis", "hta", "dv","dp" )]


##############The function that does the analysis###################################
#For each technology selects the groups that have a flag that they do that technology
crosstech<-function(x){grpcnts<-subset(grpcnt, grpcnt[, c(x)]==1)

#Calculates how many of the groups that related to technology y are also involved in the other
#technologies
aggdata1 <-apply(grpcnts,2,sum, na.rm=TRUE)#

#Returns the results
aggdata1

}
#####################################################################################
#creates a matrix of the technology names to loop over 
f<-as.matrix(names(grpcnt), nrow=length(names(grpcnt)), ncol==1)
#####################################################################################


#Works through each of the different kind of technologies applying the crosstech function
G<-apply(f,1,crosstech)

#Adds in the column names
colnames(G)<-names(grpcnt)

#Converts to a data frame
G<-as.data.frame(G)

#G is a symmetric matrix where each column/row represents a different technology and the elements x,y
#of the matrix are the number of groups that use both technology x and technology y

