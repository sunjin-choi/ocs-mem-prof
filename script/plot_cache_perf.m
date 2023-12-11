clear all;
% Specify the directory containing the CSV files
directory = '../cache_results/';

% List all CSV files in the directory
csvFiles = dir(fullfile(directory, '*.csv'));

% Initialize an empty table for concatenation
allData = [];

% Loop through each file and concatenate
for i = 1:length(csvFiles)
    % Full path to the CSV file
    filePath = fullfile(directory, csvFiles(i).name);
    
    % Read the CSV file
    tbl = readtable(filePath);
    
    % Concatenate with the existing data
    if isempty(allData)
        allData = tbl;
    else
        allData = [allData; tbl];
    end
end



% Get unique values for CacheName and TraceFile
uniqueCacheNames = unique(allData.CacheName);
uniqueTraceFiles = unique(allData.TraceFile);

% Initialize data for plotting
dataMatrix1 = zeros(length(uniqueTraceFiles), length(uniqueCacheNames)); % For num_misses1
dataMatrix2 = zeros(length(uniqueTraceFiles), length(uniqueCacheNames)); % For num_misses2

% Fill in the data for plotting
for i = 1:length(uniqueTraceFiles)
    for j = 1:length(uniqueCacheNames)
        % Find rows that match the current combination of TraceFile and CacheName
        idx = strcmp(allData.TraceFile, uniqueTraceFiles(i)) & strcmp(allData.CacheName, uniqueCacheNames(j));
        
        if any(idx)
            dataMatrix1(i, j) = sum(allData.NFMMisses(idx)); % Aggregate num_misses1
            dataMatrix2(i, j) = sum(allData.BackingStoreMisses(idx)); % Aggregate num_misses2
        end
    end
end
% Assuming you have the data in the correct format as before:

% Plot the data
figure;
hb = bar(dataMatrix1, 'grouped'); % Plot the first set of data
hold on; % Keep the figure open to overlay the second set of data
hb2 = bar(dataMatrix2, 'grouped'); % Overlay the second set of data with a small shift

% Adjust the properties of the bars to improve clarity
for k1 = 1:length(hb)
    % Set properties for the first set of bars
    hb(k1).FaceColor = 'flat';
    hb(k1).CData = k1; % Change this to set each bar to a specific color or pattern
    hb(k1).EdgeColor = 'none'; % Remove edges to reduce visual clutter
    % Adjust the position to shift the bars closer or further from the center
    hb(k1).XOffset = hb(k1).XOffset - 0.15; 
end

% TODO figure out why these are never visible- seems like x offset isn't
% working?
for k2 = 1:length(hb2)
    % Set properties for the second set of bars
    hb2(k2).FaceColor = 'flat';
    hb2(k2).CData = k2 + length(hb); % Use a different color offset for the second set
    hb2(k2).EdgeColor = 'none'; % Remove edges to reduce visual clutter
    % Adjust the position to shift the bars closer or further from the center
    hb2(k2).XOffset = hb2(k2).XOffset + 0.15; 
end

hold off; % Release the figure

% Set the x-axis labels to be at the center of each group
xticks(1:length(uniqueTraceFiles));
xticklabels(uniqueTraceFiles);
xtickangle(45);

% Add other chart elements
% You create a new legend entry for each cache name for num_misses1 and num_misses2
legendEntries = cell(1, numel(uniqueCacheNames) * 2);
for i = 1:numel(uniqueCacheNames)
    legendEntries{i*2-1} = ['NFM Misses:' ,uniqueCacheNames{i}];
    legendEntries{i*2} = ['OCS Misses:', uniqueCacheNames{i}];
end

% Now create the legend
legend([hb, hb2], legendEntries, 'Location', 'bestoutside');

xlabel('Trace File');
ylabel('Number of Misses');
title('Number of Misses by Cache Name and Trace File');
grid on; % Optionally add grid lines for better alignment visualization
