table = document.getElementById('sort');
tableDescend = document.getElementById('sort-descend');
tableExclude = document.getElementById('sort-exclude');
tableDefault = document.getElementById('sort-default');
tableRefresh = document.getElementById('sort-refresh');
tableMulti = document.getElementById('sort-multi');
tableSortRowSet = document.getElementById('sort-row-set');
tableSortRowAuto = document.getElementById('sort-row-auto');
tableSortColumnKeys = document.getElementById('sort-column-keys');
new Tablesort(table);
new Tablesort(tableDescend, { descending: true });
new Tablesort(tableExclude);
new Tablesort(tableDefault);
new Tablesort(tableMulti);
new Tablesort(tableSortRowSet);
new Tablesort(tableSortRowAuto);
new Tablesort(tableSortColumnKeys);
var refresh = new Tablesort(tableRefresh);

var rowCount = tableRefresh.rows.length;
var row = tableRefresh.insertRow(rowCount);
var cellName = row.insertCell(0);
    cellName.innerHTML = 0;

refresh.refresh();
