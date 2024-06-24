<?php

// Controller

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Post;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
  public function test0($col)
  {
    $host = 'www.example.'.$col.'.com';
    // ruleid: laravel-command-injection
    $data = `ping -n 3 {$host}`;
    return view('user.index', ['data' => $data]);
  }

  public function okTest1($column, $user)
  {
    $host = 'www.example.com';
    // ok: laravel-command-injection
    $data = `ping -n 3 {$host}`;
    return view('user.index', ['user' => $user]);
  }

}

class ProvisionServer extends Controller
{
  public function __invoke($name)
  {
    $col = 'smth_'.$name;
    // ruleid: laravel-command-injection
    $output = system('ping -n 3 '.$col, $ret_code);
    return view('user.index', ['output', $output]);
  }
}

class OkProvisionServer extends Controller
{
  public function __invoke($name)
  {
    $col = escapeshellcmd('smth_'.$name);
    // ok: laravel-command-injection
    $output = system('ping -n 3 '.$col, $ret_code);
    return view('user.index', ['output', $output]);
  }
}

// Router

use Illuminate\Support\Facades\Route;

Route::get('/posts/{type}/{page}', function ($type, $page) {
  $output = null;
  $retval = null;
  // ruleid: laravel-command-injection
  exec('ls -lah '.$type, $output, $retval);
  return view('user.index', ['result', $output]);
});

Route::match(['get', 'post'], '/smth/{type}/{page}', function ($type, $page) {
  $cmd = "/path/to/".$type;
  $args = array("foo", "bar");
  // ruleid: laravel-command-injection
  pcntl_exec($cmd, $args);

  return view('user.index', ['result']);
});

Route::get('/posts-ok/{post}', function ($name) {
  $output = null;
  $retval = null;
  // ok: laravel-command-injection
  exec('ls -lah '.escapeshellarg($name), $output, $retval);
  return view('user.index', ['result', $output]);
});

// Middleware

use Illuminate\Http\Request;

class AfterMiddleware
{
  public function handle($request, Closure $next)
  {
    $response = $next($request);
    $data = $request->input('col');
    // ruleid: laravel-command-injection
    passthru("docker-compose -f docker-compose.yml ".$data, $ret);
    log($ret);
    return $response;
  }

  protected static function getApiUserInfo(Request $request) {
    $id = $request->input('id');
    $name = $request->input('name');
    $descriptorspec = [STDIN, STDOUT, STDOUT];
    $cmd = '"findstr" "search" "'.$name.'"';
    // ruleid: laravel-command-injection
    $proc = proc_open($cmd, $descriptorspec, $pipes);
    proc_close($proc);
    return do_smth();
  }

  protected static function okGetApiUserInfo(Request $request) {
    $response = $next($request);
    $data = $request->input('col');
    // ok: laravel-command-injection
    passthru("docker-compose -f docker-compose.yml bash", $ret);
    log($ret);
    return do_smth($orders);
  }
}

// FormRequest
use Illuminate\Foundation\Http\FormRequest;

class TestRequest extends FormRequest
{
    public function rules()
    {
      $name = $this->input('name');
      // ruleid: laravel-command-injection
      $handle = popen('/path/to/'.$name.' 2>&1', 'r');
      $rule = do_smth($handle);

      // ok: laravel-command-injection
      $okHandle = popen('/path/to/'.escapeshellarg($name).' 2>&1', 'r');
      $okRule = do_smth($handle);

      return [
        'orders' => [
          'required',
          $rule,
          $okRule,
        ]
      ];
    }
}

// example from https://github.com/freescout-helpdesk/freescout/blob/HEAD/public/tools.php
if (!empty($_POST)) {
  $php_path = $_POST['php_path'];

    if (!function_exists('shell_exec')) {
      $alerts[] = [
          'type' => 'danger',
          'text' => '<code>shell_exec</code> function is unavailable. Can not run updating.',
      ];
    } else {
      try {
        // ruleid: laravel-command-injection
        $output = shell_exec($php_path.' '.$root_dir.'artisan freescout:update --force');

        // ok: laravel-command-injection
        $output = shell_exec(escapeshellcmd($php_path_sanitized.' '.$root_dir.'artisan freescout:update --force'));

        // ok: laravel-command-injection
        $output = shell_exec(escapeshellarg($php_path_sanitized).' '.$root_dir.'artisan freescout:update --force');
      } catch (\Exception $e) {
          $alerts[] = [
              'type' => 'danger',
              'text' => 'Error occured: '.htmlspecialchars($e->getMessage()),
          ];
      }
    }
}
