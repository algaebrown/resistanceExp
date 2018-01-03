# add to path: the library
for a in /home/hermuba/bin/JOELib2-alpha-20070215/lib/*.jar
do
    TMACCCP=$TMACCCP:$a
done

# add to path: tmacc itself
TMACCCP=$TMACCCP:/home/hermuba/bin/tmacc.jar
echo $TMACCCP
# run it
java -cp $TMACCCP ac.nott.tmacc.TmaccMaker /home/hermuba/data/drug/all_five_sdf.sdf ACTIVITY all_five.csv
java -cp $TMACCCP ac.nott.tmacc.TmaccMaker /home/hermuba/data/drug/all_rand_sdf.sdf ACTIVITY all_rand.csv
java -cp $TMACCCP ac.nott.tmacc.TmaccMaker /home/hermuba/data/drug/all_five_sdf.sdf ACTIVITY all_five.fgram
java -cp $TMACCCP ac.nott.tmacc.TmaccMaker /home/hermuba/data/drug/all_rand_sdf.sdf ACTIVITY all_rand.fgram
