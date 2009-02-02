# Utility functions for nagios-http

package Nagios::HTTP::Util;

use strict;
use Digest::SHA qw(sha256_base64);
use Carp;

sub gen_hash {
  my (%arg) = @_;
  my $cmd = delete $arg{cmd};
  my $freq = delete $arg{freq};
  croak "Invalid arguments to gen_hash: " . join(',', keys %arg) if keys %arg;
  croak "Missing 'cmd' argument to gen_hash" unless $cmd;
  croak "Missing 'freq' argument to gen_hash" unless $cmd;

  my $string = $cmd . \000 . $freq;
  return sha256_base64( $string );
}

1;

