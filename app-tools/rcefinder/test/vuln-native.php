<?php

function bad1() {
    $user_input = $_REQUEST["cmd"];

    // ruleid: tainted-command-injection
    system($user_input);

    // ruleid: tainted-command-injection
    shell_exec($user_input);

    // ruleid: tainted-command-injection
    exec($user_input);

    if(isset($_GET['cmd'])){
        // ruleid: tainted-command-injection
        popen($_GET['cmd'],'r');
    }

    // ruleid: tainted-command-injection
    $cmd = `$user_input`;

    $descriptorspec=array( //This index array specifies that you want to use proc_ Descriptor of the child process created by open
        0=>array('pipe','r'), //STDIN
        1=>array('pipe','w'),//STDOUT
        2=>array('pipe','w') //STDERROR
        );

        // ruleid: tainted-command-injection
        $handle=proc_open($user_input,$descriptorspec,$pipes,NULL);
        //Saved in $pipes is the file pointer corresponding to the PHP end of the pipeline created by the child process ($specified by $descriptorspec)
        if(!is_resource($handle)){
        die('proc_open failed');
        }
        //fwrite($pipes[0],'ipconfig');
        print('stdout:<br/>');
        while($s=fgets($pipes[1])){
        print_r($s);
        }
        print('===========<br/>stderr:<br/>');
        while($s=fgets($pipes[2])){
        print_r($s);
        }
        fclose($pipes[0]);
        fclose($pipes[1]);
        fclose($pipes[2]);
        proc_close($handle);
}

function ok1() {
    // ok: tainted-command-injection
    exec('echo "OK"');

    $env_var = $_ENV["cmd"];

    // ok: tainted-command-injection
    exec($env_var);
}

?>
