#!/usr/bin/env perl

use strict;
use warnings;

my @output = `df`;

sub print_line {
    my (@cols) = @_;
    $cols[4] =~ s/%//;
    print "\"$cols[5]\": {\n";
    print "\"total\": $cols[1],\n";
    print "\"used\": $cols[2],\n";
    print "\"available\": $cols[3],\n";
    print "\"device\": \"$cols[0]\",\n";
    print "\"use%\": $cols[4]\n";
    print "}\n";
}

print "{\n";
foreach my $line (@output[1..(scalar(@output) - 2)]) {
    my @cols = split(/\s+/, $line);
    print_line(@cols);
    print ','
}

print_line(split(/\s+/, $output[-1]));

print "}\n";
