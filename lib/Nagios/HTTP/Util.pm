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
  my $cmd = delete $arg{cmd};
  my $freq = delete $arg{freq};
  my $verbose = delete $arg{verbose};
  croak "Invalid arguments to gen_hash: " . join(',', keys %arg) if keys %arg;
  croak "Missing 'cmd' argument to gen_hash" unless $cmd;
  croak "Missing 'freq' argument to gen_hash" unless $cmd;

  my $string = trim($cmd) . "\000" . ($freq || '');
  my $hash = sha256_base64( $string );
  print STDERR "+ gen_hash: string '$string' -> hash '$hash'\n" if $verbose;
}

1;

