document.getElementById("Download").addEventListener("click", function () {
	var html = document.querySelector("table").outerHTML;//get 
	htmlToCSV(html, "report.csv"); //call the function
});

function htmlToCSV(html, filename) {
	var data = [];
	var rows = document.querySelectorAll("table tr");
			
	for (var i = 0; i < rows.length; i++) {
		var row = [], cols = rows[i].querySelectorAll("td, th");
				
		for (var j = 0; j < cols.length; j++) {
		        row.push(cols[j].innerText);
        }
		        
		data.push(row.join(",")); 		
	}

	downloadCSVFile(data.join("\n"), filename);
}

function downloadCSVFile(csv, filename) {
	var csv_file, download_link;

	csv_file = new Blob([csv], {type: "text/csv"});

	download_link = document.createElement("a");

	download_link.download = filename;

	download_link.href = window.URL.createObjectURL(csv_file);

	download_link.style.display = "none";

	document.body.appendChild(download_link);

	download_link.click();
}

//Adopted and modified from: 
//MEHRA, A., 2021. Export HTML Table to CSV Using JavaScript JAVASCRIPT. [online] Your Blog Coach. Available at: <https://yourblogcoach.com/export-html-table-to-csv-using-javascript/> [Accessed 7 February 2022].