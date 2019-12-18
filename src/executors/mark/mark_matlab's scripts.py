#######################################
## Annotate all experiments in sheet ## 
#######################################

## Add 4 columns at the beginning of an excel file for further analyze.
## The excel file is chosen by the user during the running.
## The names of the sheets, must be: data  sheet: 'Nuc_cell_TMRE_MITOTRACKER' 
## plate sheet: 'Plate'
## The amended excel table will be added as a new sheet at the same excel
## file: 'anotated_data'

## get dir of xls with GUI ##

from tkinter import filedialog
from tkinter import *
def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)

root = Tk()
folder_path = StringVar()
lbl1 = Label(master=root,textvariable=folder_path)
lbl1.grid(row=0, column=1)
button2 = Button(text="Browse", command=browse_button)
button2.grid(row=0, column=3)

mainloop()

## get dir of xls by specifying a folder_path and looping on all of it's '.xls' files ##

cwd = os.getcwd()
os.chdir()

#BaseFolder='D:\IftachN14\Desktop\DQE\Phenotyping Assay\Data\DQE';
#FileList=dir(sprintf('%s\\*.xls*',BaseFolder));
#cd(BaseFolder);

for ii=1:1:size(FileList,1)                                                 ## looping on files
    FileName=FileList(ii).name;
    fprintf('Parsing file #%d out of %d\n',ii,size(FileList,1));
    [STATUS,SHEETS] = xlsfinfo(FileName);                                      % for how many sheets 
end


## annotating sheet#3 to new sheet(#5) in the xls, by using sheet #4 (inserted in manually) ##

function[]=annotate_excel_scriptL(FileName)  

#[FileName,pathname] = uigetfile({'*.xlsx; *.xls'},'Open EXCEL File');
#cd(pathname);

datasheet  = 'Nuc_cell_TMRE_MITOTRACKER';
platesheet = 'Sheet1';

[~,platemat,~] = xlsread(FileName,platesheet);  % reads the specified worksheet and returns the numeric data in a matrix.
[~,~,datamat]  = xlsread(FileName,datasheet);
disp(sprintf('Annotating %s',FileName));
% -------------------------------------------------------------------------
% generate a 2D matrices, that includes all data from the plate 
% (that can be copied to the correct lines in the data table)

% initialization

patients = platemat(3:2:14,3:12);                       %Taking conditions names by plate structure (healthy or disease)
serialnum = platemat(4:2:14,3:12);                      %Taking samples serial # by plate structure

%--------------------------------------------------------------------------
% extract numbers and letters from the data matrix 
rownum = size(datamat,1);                               % # of observations per plate -2          

section = datamat(:,1);                                 %sample type (not unique)

for row = 3:rownum  
    numvec{row-2} = section{row}(5:6);
    letvec{row-2} = section{row}(1);
end
% convert strings to numbers
numvec_num = cellfun(@str2num,numvec);
letvec_num = cellfun(@int8,letvec);

%--------------------------------------------------------------------------
% connect: 

colplate = (numvec_num-1)';
rowplate = (letvec_num-int8('A'))';

%for row = 3:rownum
%    patient_out(row) = patients(rowplate(row-2),colplate(row-2));
%    serial_out(row) = serialnum(rowplate(row-2),colplate(row-2));
%end

% initialization
patient_out = cell(rownum,1);
serial_out  = cell(rownum,1);

linearInd   = sub2ind(size(patients),rowplate,colplate);
patient_out(3:end) = patients(linearInd);
serial_out(3:end)  = serialnum(linearInd);

datamat_out = [patient_out,serial_out,[' ',' ',letvec]',[' ',' ',numvec]',datamat];
%datamat_out = num2cell(datamat_out); 

final_table = cell2table(datamat_out);
%writetable(final_table,'anotated_data.txt','WriteVariableNames',false);

newfilename = sprintf('%s',FileName);

xlswrite(newfilename,datamat_out,'anotated_data1');
%xlswrite(newfilename,datamat_out,'anotated_data2');



###################################################
## Parse experiments' xls to unique files\sheets ## 
###################################################

    ## first- loop on desired directory ##

%%  call annotate_excel_scriptL(FileName, putting all xls in a specified folder for annotation

clear all;
close all;
%clc;

BaseFolder='C:\Users\MarkiMaxI\Desktop\DQE Home\Done\Annotated';
FileList=dir(sprintf('%s\\*.xls*',BaseFolder));
cd(BaseFolder);
% platesheet = 'Sheet1';

for ii=1:1:size(FileList,1)
    FileName=FileList(ii).name;
    fprintf('Parsing file #%d out of %d\n',ii,size(FileList,1));
    parseExperiment2samples(FileName)
end
% dir */*.m

                                                    ## Take folder, Disease and excel file type ##

                                                    ## for Manual parsing- file by file, with GUI ##
% %clc 
clear all
close all
% 
[FileName,pathname] = uigetfile({'*.xlsx; *.xls'},'Open EXCEL File');
cd(pathname); 

% % BaseFolder=pathname;
% % BaseFolder='C:\Users\MarkiMaxI\Desktop\DQE Home\Done\Tests';
% % FileList=dir(sprintf('%s\\*.xls*',BaseFolder));
% %FileName='';
% % cname='HC'; dname='HN'; 
% % for ii=1:1:size(FileList,1)
% %     FileName=FileList(ii).name;

                                                        ## take differemt data, positions and more numbers & go ##

fprintf('Parsing file %s',FileName);
[D,Dtxt,Draw]=xlsread(FileName,5);
stype = Dtxt(:,1); stype = stype(3:end);                        % find samples types by 'row location' (by order) 
sid   = Dtxt(:,2); sid   = sid(  3:end);                        % ID of all samples in a column
prow  = Dtxt(:,3); prow  = prow( 3:end);                        % Rows of different samples
pcol  = Dtxt(3:end,4);                                            % Columns of different samples
ids = unique(sid);
idi = unique(stype); % Unique names of all samples
Nid = length(ids);                                              %how many samples
Nfeat= size(Dtxt(2,7:end),2);

                                                                    ## prepare data for writing  
for i = 1:1:size(idi)         %Nid
    clear dTemp;
    dTemp=Draw(1:2,:);                                          %Take first two rows
    SNname=idi{i,1};        %Sname=SNname(1:end-1);
    disp(SNname)                                                %Take current sample name
%         dTemp(3:size(indid{1,i},1),1)=samtype(i);                 %put current sample type in column 1               
%         dTemp(3:size(indid{1,i},1),2)=Sname;                      %put current sample name in column 2                                                       
    kk=3;
    for jj=1:1:size(Draw,1)
        if strcmp(SNname,Draw{jj,1})
%                 exp=1;
%                 dTemp(kk,:)=Draw(jj,:);
            dTemp(kk,1)=Draw(jj,1); 
            dTemp(kk,2)=Draw(jj,2);
            dTemp(kk,3)=Draw(jj,3);
            dTemp(kk,4)=Draw(jj,4);
            dTemp(kk,5)=Dtxt(jj,5);
%                 dTemp(kk,6:end)=[{D(jj,3:end)}];
            for j=1:1:(Nfeat+1)
                dTemp(kk,5+j)=[{D(jj-2,j+2)}];
            end
            kk=kk+1;
%             else exp=0;
        end
    end
%         if exp==1
        name=sprintf('%s_%s.xls',SNname,FileName(1:4)); %Sname=Sname(1:end-1); 
        name=strrep(name,'/','_'); name=strrep(name,'\','_');

        % put by sample xls's elswhere

        folder = sprintf('%s',FileName(1:5));   %VALIDATEEEEEE name
        if ~exist(folder, 'dir')
            mkdir(folder);
        end
%             baseFileName = 'diagramm.xlsx';
        fullFileName = fullfile(folder, name);
        status = xlswrite(fullFileName,dTemp);
%             xlswrite(fullFileName ,vector_1,'Fluid');
%             xlswrite(fullFileName ,vector_2,'Power');
%             status = xlswrite(name,dTemp);
        disp(status)
end


######################################################
## Name ER-LYSO plates with correct channels' names ## 
######################################################

%% Change features names; Mito To ER%%

clear all;
close all;
%clc;

BaseFolder='C:\Users\MarkiMaxI\Desktop\DQE Home\Done\Annotated\ER LYSO';
% FileList=dir(sprintf('%s\\*.xls*',BaseFolder));
cd(BaseFolder);
FileList=dir('*/*.xls');

for i=1:1:length(FileList)
     FileName=FileList(i).name;
     FileLoc =FileList(i).folder;
     cd(FileLoc);
     [D,Dtxt,Draw]=xlsread(FileName);
     fprintf('Replacing features names in file %s',FileName);
     for j=7:1:45
         if contains(Draw{2,j},'TMRE')
                Draw{2,j}=strrep(Draw{2,j},'TMRE','ER');
         elseif contains(Draw{2,j},'MITO')
                Draw{2,j}=strrep(Draw{2,j},'MITO','LYSO');
         elseif contains(Draw{2,j},'MITOTRACKER')
                Draw{2,j}=strrep(Draw{2,j},'MITOTRACKER','LYSO');
         elseif contains(Draw{2,j},'MITOTRECKER')
                Draw{2,j}=strrep(Draw{2,j},'MITOTRECKER','LYSO');  
         end
     end
     status = xlswrite(FileName,Draw)
end


######################
## KStest versions1 ## 
######################

%% KS test between two plates (wellBywell) or in plate comparison
%The asymptotic p-value becomes very accurate for large sample sizes, and is believed to be reasonably accurate 
%for sample sizes n1 and n2, such that (n1*n2)/(n1 + n2) ? 4.

clear all
close all

CompRowsSamePlate = 1;               % 1 for the Same plate + chosen well to be compared to, 0 for two plate- WELLbyWELL
CompWell = 'D';
[filename1,pathname1] = uigetfile({'*.xlsx; *.xls'},'Open EXCEL File');
cd(pathname1);
fname1 = filename1;
fname1x=[pathname1 fname1];                        % File #1 location
[D1,Dtxt1,Draw1]=xlsread([fname1x], 5);            % Read data from excel 
if CompRowsSamePlate
    fname2=fname1;
    fname2x=fname1x;
    [D2,Dtxt2,Draw2]=xlsread([fname1x], 5);
else
    [filename2,pathname2] = uigetfile({'*.xlsx; *.xls'},'Open EXCEL File');
    fname2 = filename2;                                                                 %excel #2
    fname2x=[pathname2 fname2];                         % File #2 location
    [D2,Dtxt2,Draw2]=xlsread([fname2x], 5);             % Read data from excel
end

Dtxt1(3:end,4)=num2cell(D1(:,1));
Dtxt2(3:end,4)=num2cell(D2(:,1));

FeaturesNames=Dtxt1(2,7:45);                            % taking features name

%counting wells
counter=1;
for ii='B':'G'
    for jj=2:1:11
        WellsNames{counter}=sprintf('%s%d',ii,jj);      % sprintf Write formatted data to string or character vector
        counter=counter+1;
    end;
end;

for ii=1:1:size(FeaturesNames,2)
    for jj=1:1:length(WellsNames)
        TempName=FeaturesNames{ii};
        TempName(find(FeaturesNames{ii}==' '))='_';         %cant use spaces in struct: switching spaces to _ seperation
        %%%buliding struct of all features to each well
        AllWells.(WellsNames{jj}).Features.(TempName)=[];   
    end;
end;

counter=1;
NaorCounter=1;
%discarded = strcu(6,10)

for ii= setdiff(['B' 'C' 'D' 'E' 'F' 'G'], CompWell)                    %Ccomparison to chosen well  
    for jj=2:1:11
        RowLoc=find(ismember(Dtxt1(3:end,3),ii));
        ColLoc=find([cell2mat(Dtxt1(3:end,4))]'==jj);
        OrigCellLoc1=intersect(RowLoc,ColLoc);
        
        if CompRowsSamePlate
            RowLoc=find(ismember(Dtxt2(3:end,3),CompWell));                %taking chosen well
        else
            RowLoc=find(ismember(Dtxt2(3:end,3),ii));                       %or other plate
        end
        
        ColLoc=find([cell2mat(Dtxt2(3:end,4))]'==jj);
        OrigCellLoc2=intersect(RowLoc,ColLoc);

        n1 = length(OrigCellLoc1); 
        n2 = length(OrigCellLoc2);
        num2perm=min(n1,n2);
        permsel1=randperm(length(OrigCellLoc1),num2perm);
        permsel2=randperm(length(OrigCellLoc2),num2perm);
        CellLoc1=permsel1;
        CellLoc2=permsel2;
        %AllWells(NaorCounter).Well=sprintf('%s%d',ii,jj);
        for kk=4:1:size(D1,2)
            if ~isempty(D1(CellLoc1,kk)) && ~isempty(D2(CellLoc2,kk))
                TempName=FeaturesNames{kk-3};
                TempName(find(FeaturesNames{kk-3}==' '))='_';
                
                AllWells.(WellsNames{NaorCounter}).Features.(TempName)=kstest2(D1(CellLoc1,kk),D2(CellLoc2,kk),'alpha',0.001);    %KStest result of the hypothesis test 
               [KStest(NaorCounter, kk-3),P(NaorCounter, kk-3), KSSTAT(NaorCounter, kk-3)]=kstest2(D1(CellLoc1,kk),D2(CellLoc2,kk),'alpha',0.001);
               
             % nullify P values for tests with too few cells or very
             % different num of cells
             
               %fprintf(1, '%s  %d %d %.5f\n', TempName, n1, n2, abs(log(n1/n2)));
              if (min(n1, n2) < 50) % || (abs(log(n1/n2)) > log(1.5))                       %conditions to discard
                   P(NaorCounter, kk-3) = 1.9953; %0.00001; 
%                    fprintf(1, 'Disc: %s %c %d %d %d \n', TempName,ii, jj,n1, n2);
       
                   %discarded(kk-3)=fprintf('%c %d\n',ii,jj);
                 %  discarded(kk)=('Discarding %c %d\n', ii, jj);
               end
               
             % if strfind(TempName, 'NUC')          % Choose a feature by name
               %% plot distributions in HIST
%                [h1,x1] = hist(D1(CellLoc1,kk), 50);
%                [h2,x2] = hist(D2(CellLoc2,kk), 50);
%                figure(7); clf; plot(x1, h1, 'b', x2, h2, 'r'); 
%                title(sprintf('%s  p = %.4f  log10P = %.2f', TempName, P(NaorCounter, kk-3), log10(P(NaorCounter, kk-3))));  
%                xlabel(sprintf('%c %d  n1 = %d  n2 = %d', ii, jj, n1, n2));
               %keyboard; 
               %pause;
               %saveas(gcf,ii for ii in 'FeaturesNames(1,ii).bmp')
               %end %%%%%%
            end;
        end;
  %      keyboard;            
        NaorCounter=NaorCounter+1;
     
        %D1Means(counter, jj,:)= mean(D1(CellLoc1,4:end)); 
        %D2Means(counter, jj,:)= mean(D2(CellLoc2,4:end));
 
    end;
    counter=counter+1;
end;

climits = [-4 0.3];      %colormap limits

figure(1); clf; hold on;

for ii=1:1:size(P,2)
    subplot(10,4,ii)
    ReMat=reshape(P(:,ii),size(P,1)./10,10);
    logReMat = log10(ReMat);
    imagesc(logReMat, climits);
    c = colormap(parula);
    colormap([c ;1 1 1]);

    title(FeaturesNames(1,ii))
    if ii==39
        break;
    end;
end;
colorbar('South');

figure(5); clf; 
imagesc(log(P), climits); colorbar;
c = colormap;
colormap([c; 1 1 1]);

pp = sum(P);
sum(pp)
%AllWells=struct('Well','');
%for kk=4:1:size(D1,2)


################################################
## KStest (versionsX2), Anderson-Darling test ## 
################################################


%% KS test between two plates - VersionII (wells-10Vs10) 
%Mark M ver1, 16.07.17

clear all
close all

[filename1,pathname1] = uigetfile({'*.xlsx; *.xls'},'Open EXCEL File');
cd(pathname1);
fname1 = filename1
fname1x=[pathname1 fname1];                                           %File #1 location
[D1,Dtxt1,Draw1]=xlsread([fname1x], 5);                               % Read data from excel 
[filename2,pathname2] = uigetfile({'*.xlsx; *.xls'},'Open EXCEL File');
fname2 = filename2;                                                   %excel #2
fname2x=[pathname2 fname2];                                           %File #2 location
[D2,Dtxt2,Draw2]=xlsread([fname2x], 5);                               % Read data from excel   

Dtxt1(3:end,4)=num2cell(D1(:,1));
Dtxt2(3:end,4)=num2cell(D2(:,1));

FeaturesNames=Dtxt1(2,7:45);                         %taking features name

%counting wells
counter=1;
for ii='B':'G'
    for jj=2:1:11
        WellsNames{counter}=sprintf('%s%d',ii,jj);   %sprintf Write formatted data to string or character vector
        counter=counter+1;
    end;
end;

for ii=1:1:size(FeaturesNames,2)
    for jj=1:1:length(WellsNames)
        TempName=FeaturesNames{ii};
        TempName(find(FeaturesNames{ii}==' '))='_';         %cant use spaces in struct: switching spaces to _ seperation
        %%%buliding struct of all features to each well
        AllWells.(WellsNames{jj}).Features.(TempName)=[];   
    end;
end;

counter=1;
NaorCounter=1;
%discarded = strcu(6,10)

Column1=[1];Column2=[1];

for jj=2:1:11          
        ColLoc1=find([cell2mat(Dtxt1(3:end,4))]'==jj);
        ColLoc2=find([cell2mat(Dtxt2(3:end,4))]'==jj);
        n1 = length(ColLoc1); 
        n2 = length(ColLoc2);
        num2perm=min(n1,n2);
        permsel1=randperm(length(ColLoc1),num2perm);
        permsel2=randperm(length(ColLoc2),num2perm);
        CellLoc1=permsel1;
        CellLoc2=permsel2;
        
        %AllWells(NaorCounter).Well=sprintf('%s%d',ii,jj);
        for kk=4:1:size(D1,2)
            if ~isempty(D1(CellLoc1,kk)) && ~isempty(D2(CellLoc2,kk))
                TempName=FeaturesNames{kk-3};
                TempName(find(FeaturesNames{kk-3}==' '))='_';
                
                AllWells.(WellsNames{NaorCounter}).Features.(TempName)=kstest2(D1(CellLoc1,kk),D2(CellLoc2,kk),'alpha',0.001);    %KStest result of the hypothesis test 
               [KStest(NaorCounter, kk-3),P(NaorCounter, kk-3), KSSTAT(NaorCounter, kk-3)]=kstest2(D1(CellLoc1,kk),D2(CellLoc2,kk),'alpha',0.001);
               
             % nullify P values for tests with too few cells or very
             % different num of cells
             
               fprintf(1, '%s  %d %d %.5f\n', TempName, n1, n2, abs(log(n1/n2)));
%               if (min(n1, n2) < 640) % || (abs(log(n1/n2)) > log(1.5))                       %conditions to discard
%                    P(NaorCounter, kk-3) = 1.9953; %0.00001; 
%                    fprintf(1, 'Disc: %s %c %d %d %d \n', TempName,ii,jj,n1, n2);
       
                   %discarded(kk-3)=fprintf('%c %d\n',ii,jj);
                 %  discarded(kk)=('Discarding %c %d\n', ii, jj);
%                end
               
             % if strfind(TempName, 'NUC')          % Choose a feature by name
               
%                [h1,x1] = hist(D1(CellLoc1,kk), 50);
%                [h2,x2] = hist(D2(CellLoc2,kk), 50);
%                figure(7); clf; plot(x1, h1, 'b', x2, h2, 'r'); 
%                title(sprintf('%s  p = %.4f  log10P = %.2f', TempName, P(NaorCounter, kk-3), log10(P(NaorCounter, kk-3))));  
%                xlabel(sprintf('%c %d  n1 = %d  n2 = %d', ii, jj, n1, n2));
               
               %pause;
               %saveas(gcf,ii for ii in 'FeaturesNames(1,ii).bmp')
               %end %%%%%%
            end;
        end;
  %      keyboard;            
        NaorCounter=NaorCounter+1;
 
    end;
counter=counter+1;
   
climits = [-4 0.3];      %colormap limits

figure(1); clf; hold on;

for ii=1:1:size(P,2)
    subplot(10,4,ii)
    ReMat=reshape(P(:,ii),size(P,1)./10,10);
    logReMat = log10(ReMat);
    imagesc(logReMat, climits);
    c = colormap(parula);
    colormap([c ;1 1 1]);

    title(FeaturesNames(1,ii))
    if ii==39
        break;
    end;
end;
colorbar('South');

figure(5); clf; 
imagesc(log(P), climits); colorbar;
c = colormap;
colormap([c; 1 1 1]);

%AllWells=struct('Well','');
%for kk=4:1:size(D1,2)
%D1Means(counter, jj,:)= mean(D1(CellLoc1,4:end)); 
%D2Means(counter, jj,:)= mean(D2(CellLoc2,4:end));


##########################
## Get Data from Parsed ## 
##########################


% function [X,Z,Y,NiceColors]= getdata_parsed
% gather data from parsed experiments from a specific folder and subfolder 
% Mark v2[2019]
% loop on files and take data, coloring and holders

%when not function
if (1)
    close all
    clear all
end

BaseFolder='C:\Users\MarkiMaxI\Desktop\DQE Home\Done\Annotated\Mito TMRE';
cd(BaseFolder);
FileList=dir('*/*.xls'); 
X=[]; color=[]; KeepSizeD=[]; 

resdir = ['all samples plots'];
mkdir(resdir);

% AllNames=[];
HealCount=0; SickCount=0; HealOrSick=[];
mm=1;               % loop for inserting first to rows 
% XLabelWithNum={1,size(FileList,1)};
for ii=1:1:size(FileList,1)
    FileName=FileList(ii).name;
    FileLoc =FileList(ii).folder;
    cd(FileLoc);
    Sname = FileName;     %%
    fprintf('Taking data from file %s (#%d out of #%d)\n',Sname,ii,size(FileList,1));
    [D,Dtxt,Draw]=xlsread(FileList(ii).name);
    Features=Draw(2,7:end);
    
    for kk=1:1:39
        allmean(kk) = mean(D(:,3+kk));
        allstd(kk) = std(D(:,3+kk)) ;
        allmedian(kk) = median(D(:,3+kk)) ;
        XLabelWithNum{kk}=sprintf('%s, mean=%d std=%d median=%d',Features{kk,1},allmean,allstd, allmedian);
    end
    NumSamp=size(D,1);
%     XLabelWithNum{}=sprintf('%s, n=%d mean=%d std=%d median=%d',FileName,NumSamp,allmean,allstd, allmedian);
    boxplot(D(:,4:end));
    set(gca, 'YScale', 'log');
    set(gca,'XTickLabel',XLabelWithNum)
    set(gca,'FontSize',9)
    set(gca,'XTickLabelRotation',18)
    ylabel('Log scale'); 
    title(sprintf('%s features boxplots, n=%d',FileName,NumSamp)); 
%     XSplitLables{2*(kk-1)+1}=sprintf('%s, n=%d',ids{kk},NumSamp(kk));
%         XSplitLables{2*(kk-1)+2}=sprintf(' mean=%d std=%dd',allmean(kk),allstd(kk));
    print('-dpng',[resdir '\' Sname '.png']);
    
    %Control or Condition of sample
    
    if contains(Draw{3,1},'HC')%strcmp(Draw{3,1}(1:end),'HC') %If sample is healthy
        Hcol=[0 0 1];
        Hsymbol = 's';
        HealCount=HealCount+1;
        HealOrSick(ii)=1;
    else                                               %If sample is sick
        Hcol=[1 0 0];
        Hsymbol = 'o';
        SickCount=SickCount+1;
        HealOrSick(ii)=0;
    end
    
    %KeepLast=size(AllNames,1)
    %AllNames{KeepLast+1:KeepLast+size(D(4:end,:),1)-1}=Sname;
    if mm==1
        X=[X ; Draw];
        mm=0
    end
    X=[X ; Draw(3:end,:)];
    KeepSizeD(ii)=size(D(3:end,:),1);
end

% Colors for each sample

Hcount=1; Scount=1;
for jj=1:1:length(HealOrSick)
    if (HealOrSick(jj)) % if healthy
        NiceColors{jj}=[0 0.15 Hcount/HealCount];
        Hcount=Hcount+1;
    else
        NiceColors{jj}=[Scount/SickCount 0.85 0];
        Scount=Scount+1;
    end
end

Z=X(3:end,7:end);
Y=cell2mat(Z);

% end


#############################
## BoxPlot parsed and more ## 
#############################



%%Take data from folder and sub-f's all parsed xlss
%% first- get data matrix and sample coloring
if (1)
    clear all
end
close all
%clc;
%warning off

[X,Z,Y,NiceColors]=getdata_parsed;
% BaseFolder='C:\Users\MarkiMaxI\Desktop\DQE Home\Done\Annotated\Mito TMRE';
% cd(BaseFolder);
% FileList=dir('*/*.xls'); 
% [X,Z,Y,NiceColors]=get_data;

%% Gather data for plot
 
stype = X(3:end,1); %stype = stype(3:end);                        % Disease or Healthy 
sid   = X(3:end,2); %sid   = sid(  3:end);                        % ID of all samples (HC&sick)
prow  = X(3:end,3); %prow  = prow( 3:end);                        % row of all samples
pcol  =        X(:,4);                                               % column of all samples
ids = unique(sid);                                                   % Final samples names (unique)
Nid = length(ids);                                                   % number of different samples
idi = unique(stype);                                                 % different categories of samples

%% DO what
a=1;b=1;
for j=1:1:length(idi)
    if startsWith(idi{j,1},'HC')    % idi{j,1}=='HC'|'Hc'
        cname{a} = idi{j,1};
        a=a+1;
%         dname = idi{2,1};
    else;
%         cname = idi{2,1};
        dname{b} = idi{j,1};
        b=b+1;
    end
end

for i = 1:1:Nid                                                   % looping on different samples
    indid{i} = find(strcmp(sid,ids{i}));                        % find all cells of sample i - by Sample
    samtype(i) = stype(indid{i}(1));                            % put sample with currect grouping 
end

for ll = 1:1:size(idi,1)                                                   % looping on different samples
    indi{ll} = find(strcmp(stype,idi{ll}));                        % find all cells of sample i - by Group
    samtypo(ll) = stype(indi{ll}(1));                            % put sample with currect grouping 
end
%indid for observations' counts
% 
% for jj = 1:1:length(ids)
%     amind = find(strcmp(samtype(jj), cname));                          
% %     csamind = find(strcmp(samtype(jj), cname));                          % put control correct sample indices for cind
% %     dsamind = find(strcmp(samtype(jj), dname));                          % put disease correct sample indices for dind
% end


% cind = [];
% for i = csamind(:)'
%     cind = [cind ; indid{i}];                                   % match all control pointers 
% end
% 
% dind = [];
% for i = dsamind(:)'
%     dind = [dind ; indid{i}];                                   % match all disease pointers 
% end

%% Plot features for controls, patients as boxplots
resdir = ['all samples plots'];
mkdir(resdir);
features=X(2,7:end);
Nfeat=length(features);

clear XLabelWithNum;
for fi = 1:Nfeat                                  % index of feature 
    figure(1); 
    
    for kk=1:1:length(ids)                          % indid 1,2,3: healthy
       allmean(kk) = mean(Y(find(ismember(sid,ids{kk})),fi)) ;
       allstd(kk) = std(Y(find(ismember(sid,ids{kk})),fi)) ;
       allmedian(kk) = median(Y(find(ismember(sid,ids{kk})),fi)) ;
       NumSamp(kk)=length(find(ismember(sid,ids{kk})));
       XLabelWithNum{kk}=sprintf('%s, n=%d mean=%d std=%d',ids{kk},NumSamp(kk),allmean(kk),allstd(kk));
    
       featname = X{2, fi + 6};
       
       boxplot([Y(indid{1,kk}, fi)]);
       hold on
    %Y(ids{kk}, fi)], stype([indid; ids(kk)]));                %which column to plot
    %boxplot([D(dind, fi+3); D(cind, fi+3)], sid([dind; cind]));
    
        set(gca,'XTickLabel',XLabelWithNum)
        set(gca,'FontSize',9)
        set(gca,'XTickLabelRotation',18)
        ylabel(featname); 
        title('Write What You Want')            %sname(1:end-4));
        print('-dpng',[resdir '\' featname '.png']);
        %%saveas('-dpng',[resdir '\' featname '.png'])' 
        %pause;
        clf;
    end
end



##################
## Violion plot ## 
##################



##################
## PCA and tSNE ## 
##################

## %%  Hotelling's T2, a statistical measure of the multivariate distance of each observation from the center of the data set...
...This is an analytical way to find the most extreme points in the data. ##
## with and w\o VariableWeights ##



##############################
## Coloring Samples Uniquly ## 
##############################

X=[]; color=[]; KeepSizeD=[]; AllNames=[];
HealCount=0; SickCount=0; HealOrSick=[];
AllSick=[]; AllHealthy=[];
SickHealthyInd=[];                                      %%open group fpr PDF of each population

for ii=1:1:size(FileList,1)
    FileName=FileList(ii).name;
    Sname = FileName(1:end-4);
    disp(sprintf('Processing file #%d out of %d',ii,size(FileList,1)));
    [D,Dtxt,Draw]=xlsread(FileList(ii).name);
    if strcmp(Draw{3,1}(1:end),'HC')                   %If sample is healthy
        Hcol=[0 0 1];
        Hsymbol = 's';
        HealCount=HealCount+1;
        HealOrSick(ii)=1;
        AllHealthy=[AllHealthy;D(4:end,:)];
        SickHealthyInd=[SickHealthyInd;ones(size(D(4:end,:),1),1)];
    else                                               %If sample is sick
        Hcol=[1 0 0];
        Hsymbol = 'o';
        SickCount=SickCount+1;
        HealOrSick(ii)=0;
        AllSick=[AllSick;D(4:end,:)];
        SickHealthyInd=[SickHealthyInd;zeros(size(D(4:end,:),1),1)];
    end
    X=[X ; D(4:end,:)];
    %KeepLast=size(AllNames,1)
    %AllNames{KeepLast+1:KeepLast+size(D(4:end,:),1)-1}=Sname;
    KeepSizeD(ii)=size(D(4:end,:),1);
end

%% Colors

ColorScheme=1;                                  %1 for coloring by population , 0 for coloring by sample

if (ColorScheme==0)
    Hcount=1; Scount=1;
    for jj=1:1:length(HealOrSick)
        if (HealOrSick(jj)) % if healthy
            NiceColors{jj}=[0 0 Hcount/HealCount];
            Hcount=Hcount+1;
        else
            NiceColors{jj}=[Scount/SickCount 0 0];
            Scount=Scount+1;
        end;
    end;
    
elseif ColorScheme==1
    % Hcount=1; Scount=1;
    for jj=1:1:length(HealOrSick)
        if (HealOrSick(jj)) % if healthy
            NiceColors{jj}=[0 0 1];
            %Hcount=Hcount+1;
        else
            NiceColors{jj}=[1 0 0];
            %Scount=Scount+1;
        end;
    end;    
end;
% NiceColors={[1 0 0],[0 1 0],[0 0 1],[1 1 0],[0 1 1],[1 0 1],[0 0 0],[0.7 0.7 0.7],[0.4 0.7 0.4],[0.7 0.7 0.4]};
% for ii=1:1:size(FileList,1)
%NiceColors={[0 0 1],[0 0 1],[0 0 1],[0 0 1],[0 0 1],[0 0 1],[1 0 0],[1 0 0],[1 0 0],[1 0 0]};

for ii=1:1:size(FileList,1)
    KeepLast=length(color);
    color(KeepLast+1:KeepLast+KeepSizeD(ii),1:3)=ones(KeepSizeD(ii),1)*NiceColors{ii};
end;


## Create: TAKE STATS, U test, brute force enumaration ##