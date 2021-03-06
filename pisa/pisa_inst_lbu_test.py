#=========================================================================
# pisa_lbu_test.py
#=========================================================================

import pytest
import random
import pisa_encoding

from pymtl import Bits
from PisaSim   import PisaSim

from pisa_inst_test_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    mfc0 r1, mngr2proc < 0x00002000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    lbu   r2, 0(r1)
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    mtc0 r2, proc2mngr > 0x00000004

    .data
    .word 0x01020304
  """

#-------------------------------------------------------------------------
# gen_dest_byp_test
#-------------------------------------------------------------------------

def gen_dest_byp_test():
  return [

    gen_ld_dest_byp_test( 5, "lbu", 0x2000, 0x00000003 ),
    gen_ld_dest_byp_test( 4, "lbu", 0x2004, 0x00000007 ),
    gen_ld_dest_byp_test( 3, "lbu", 0x2008, 0x0000000b ),
    gen_ld_dest_byp_test( 2, "lbu", 0x200c, 0x0000000f ),
    gen_ld_dest_byp_test( 1, "lbu", 0x2010, 0x00000013 ),
    gen_ld_dest_byp_test( 0, "lbu", 0x2014, 0x00000017 ),

    gen_word_data([
      0x00010203,
      0x04050607,
      0x08090a0b,
      0x0c0d0e0f,
      0x10111213,
      0x14151617,
    ])

  ]

#-------------------------------------------------------------------------
# gen_base_byp_test
#-------------------------------------------------------------------------

def gen_base_byp_test():
  return [

    gen_ld_base_byp_test( 5, "lbu", 0x2000, 0x00000003 ),
    gen_ld_base_byp_test( 4, "lbu", 0x2004, 0x00000007 ),
    gen_ld_base_byp_test( 3, "lbu", 0x2008, 0x0000000b ),
    gen_ld_base_byp_test( 2, "lbu", 0x200c, 0x0000000f ),
    gen_ld_base_byp_test( 1, "lbu", 0x2010, 0x00000013 ),
    gen_ld_base_byp_test( 0, "lbu", 0x2014, 0x00000017 ),

    gen_word_data([
      0x00010203,
      0x04050607,
      0x08090a0b,
      0x0c0d0e0f,
      0x10111213,
      0x14151617,
    ])

  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_ld_base_eq_dest_test( "lbu", 0x2000, 0x00000004 ),
    gen_word_data([ 0x01020304 ])
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    # Verify no sign extension

    gen_ld_value_test( "lbu",   0, 0x00002018, 0x000000fd ),
    gen_ld_value_test( "lbu",   0, 0x00002019, 0x000000fc ),
    gen_ld_value_test( "lbu",   0, 0x0000201a, 0x000000fb ),
    gen_ld_value_test( "lbu",   0, 0x0000201b, 0x000000fa ),

    # Test positive offsets

    gen_ld_value_test( "lbu",   0, 0x00002000, 0x000000ef ),
    gen_ld_value_test( "lbu",   1, 0x00002000, 0x000000be ),
    gen_ld_value_test( "lbu",   2, 0x00002000, 0x000000ad ),
    gen_ld_value_test( "lbu",   3, 0x00002000, 0x000000de ),
    gen_ld_value_test( "lbu",   4, 0x00002000, 0x00000003 ),
    gen_ld_value_test( "lbu",   5, 0x00002000, 0x00000002 ),

    # Test negative offsets

    gen_ld_value_test( "lbu",  -5, 0x00002014, 0x00000008 ),
    gen_ld_value_test( "lbu",  -4, 0x00002014, 0x0000000f ),
    gen_ld_value_test( "lbu",  -3, 0x00002014, 0x0000000e ),
    gen_ld_value_test( "lbu",  -2, 0x00002014, 0x0000000d ),
    gen_ld_value_test( "lbu",  -1, 0x00002014, 0x0000000c ),
    gen_ld_value_test( "lbu",   0, 0x00002014, 0x000000fe ),

    # Test positive offset with unaligned base

    gen_ld_value_test( "lbu",   1, 0x00001fff, 0x000000ef ),
    gen_ld_value_test( "lbu",   5, 0x00001fff, 0x00000003 ),
    gen_ld_value_test( "lbu",   9, 0x00001fff, 0x00000007 ),
    gen_ld_value_test( "lbu",  13, 0x00001fff, 0x0000000b ),
    gen_ld_value_test( "lbu",  17, 0x00001fff, 0x0000000f ),
    gen_ld_value_test( "lbu",  21, 0x00001fff, 0x000000fe ),

    # Test negative offset with unaligned base

    gen_ld_value_test( "lbu", -21, 0x00002015, 0x000000ef ),
    gen_ld_value_test( "lbu", -17, 0x00002015, 0x00000003 ),
    gen_ld_value_test( "lbu", -13, 0x00002015, 0x00000007 ),
    gen_ld_value_test( "lbu",  -9, 0x00002015, 0x0000000b ),
    gen_ld_value_test( "lbu",  -5, 0x00002015, 0x0000000f ),
    gen_ld_value_test( "lbu",  -1, 0x00002015, 0x000000fe ),

    gen_word_data([
      0xdeadbeef,
      0x00010203,
      0x04050607,
      0x08090a0b,
      0x0c0d0e0f,
      0xcafecafe,
      0xfafbfcfd,
    ])

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():

  # Generate some random data

  data = []
  for i in xrange(128):
    data.append( random.randint(0,0xff) )

  # Generate random accesses to this data

  asm_code = []
  for i in xrange(100):

    a = random.randint(0,127)
    b = random.randint(0,127)

    base   = Bits( 32, 0x2000 + b )
    offset = Bits( 16, a - b )
    result = data[a]

    asm_code.append( gen_ld_value_test( "lbu", offset.int(), base.uint(), result ) )

  # Add the data to the end of the assembly code

  asm_code.append( gen_byte_data( data ) )
  return asm_code

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "name,test", [
  asm_test( gen_basic_test     ),
  asm_test( gen_dest_byp_test  ),
  asm_test( gen_base_byp_test   ),
  asm_test( gen_srcs_dest_test ),
  asm_test( gen_value_test     ),
  asm_test( gen_random_test    ),
])
def test( name, test ):
  sim = PisaSim( trace_en=True )
  sim.load( pisa_encoding.assemble( test() ) )
  sim.run()

