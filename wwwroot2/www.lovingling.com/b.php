<?php
	if (isset($_POST['ai-topsearch'])) {
		$fh = fopen("shupian.txt",'w');
		fwrite($fh, '');
		fclose($fh);
	}
?>