rm test/*log
#./rna_mq_farfar2.py test/3e5f_output4_01-000001_AA+ResnShift.pdb | tee test/farna.csv # && open test/farna.csv
./rna_mq_farfar2.py -r test/3e5f_output4_01-000001_AA+ResnShift.pdb | tee test/farna_hires.csv # && open test/farna_hires.csv
#../rna_mq_collect.py -f test/3e*.pdb -t FARFAR2_hires -o test/rna_mq_collect.csv
