# Utility functions for nagios-http

package Nagios::HTTP::Util;

use strict;
use Digest::SHA qw(sha256_base64);
use Carp;

sub trim {
  my ($str) = @_;
  $str =~ s/^\s+//;
  $str =~ s/\s+$//;
  return $str;
}

sub gen_hash {
  my (%arg) = @_;
  my $cmd     = delete $arg{cmd} 
    or croak "Missing 'cmd' argument to gen_hash\n";
  my $env     = delete $arg{env} || [];
  my $url     = delete $arg{url} || '';
  my $freq    = delete $arg{freq} || '';
  my $minute  = delete $arg{minute} || '';
  my $hour    = delete $arg{hour} || '';
  my $dow     = delete $arg{dow} || '';
  my $verbose = delete $arg{verbose};
  my $logger  = delete $arg{logger} || sub { print STDERR "+ $_[0]\n" if $verbose };
  croak "Invalid arguments to gen_hash: " . join(',', keys %arg) if keys %arg;

  my $string = join("\f", trim($cmd), $freq, $minute, $hour, $dow, $url, @$env);
  my $hash = sha256_base64( $string );
  $logger->("gen_hash: string '$string' -> hash '$hash'");
  return $hash;
}

1;

