#=========================================================================
# pisa_and_test.py
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
    mfc0 r1, mngr2proc < 0x0f0f0f0f
    mfc0 r2, mngr2proc < 0x00ff00ff
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    and r3, r1, r2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    mtc0 r3, proc2mngr > 0x000f000f
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#-------------------------------------------------------------------------
# gen_dest_byp_test
#-------------------------------------------------------------------------

def gen_dest_byp_test():
  return [
    gen_rr_dest_byp_test( 5, "and", 0x00000f0f, 0x000000ff, 0x0000000f ),
    gen_rr_dest_byp_test( 4, "and", 0x0000f0f0, 0x00000ff0, 0x000000f0 ),
    gen_rr_dest_byp_test( 3, "and", 0x000f0f00, 0x0000ff00, 0x00000f00 ),
    gen_rr_dest_byp_test( 2, "and", 0x00f0f000, 0x000ff000, 0x0000f000 ),
    gen_rr_dest_byp_test( 1, "and", 0x0f0f0000, 0x00ff0000, 0x000f0000 ),
    gen_rr_dest_byp_test( 0, "and", 0xf0f00000, 0x0ff00000, 0x00f00000 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_byp_test
#-------------------------------------------------------------------------

def gen_src0_byp_test():
  return [
    gen_rr_src0_byp_test( 5, "and", 0x0f00000f, 0xff000000, 0x0f000000 ),
    gen_rr_src0_byp_test( 4, "and", 0xf00000f0, 0xf000000f, 0xf0000000 ),
    gen_rr_src0_byp_test( 3, "and", 0x00000f0f, 0x000000ff, 0x0000000f ),
    gen_rr_src0_byp_test( 2, "and", 0x0000f0f0, 0x00000ff0, 0x000000f0 ),
    gen_rr_src0_byp_test( 1, "and", 0x000f0f00, 0x0000ff00, 0x00000f00 ),
    gen_rr_src0_byp_test( 0, "and", 0x00f0f000, 0x000ff000, 0x0000f000 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_byp_test
#-------------------------------------------------------------------------

def gen_src1_byp_test():
  return [
    gen_rr_src1_byp_test( 5, "and", 0x0f0f0000, 0x00ff0000, 0x000f0000 ),
    gen_rr_src1_byp_test( 4, "and", 0xf0f00000, 0x0ff00000, 0x00f00000 ),
    gen_rr_src1_byp_test( 3, "and", 0x0f00000f, 0xff000000, 0x0f000000 ),
    gen_rr_src1_byp_test( 2, "and", 0xf00000f0, 0xf000000f, 0xf0000000 ),
    gen_rr_src1_byp_test( 1, "and", 0x00000f0f, 0x000000ff, 0x0000000f ),
    gen_rr_src1_byp_test( 0, "and", 0x0000f0f0, 0x00000ff0, 0x000000f0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_byp_test
#-------------------------------------------------------------------------

def gen_srcs_byp_test():
  return [
    gen_rr_srcs_byp_test( 5, "and", 0x000f0f00, 0x0000ff00, 0x00000f00 ),
    gen_rr_srcs_byp_test( 4, "and", 0x00f0f000, 0x000ff000, 0x0000f000 ),
    gen_rr_srcs_byp_test( 3, "and", 0x0f0f0000, 0x00ff0000, 0x000f0000 ),
    gen_rr_srcs_byp_test( 2, "and", 0xf0f00000, 0x0ff00000, 0x00f00000 ),
    gen_rr_srcs_byp_test( 1, "and", 0x0f00000f, 0xff000000, 0x0f000000 ),
    gen_rr_srcs_byp_test( 0, "and", 0xf00000f0, 0xf000000f, 0xf0000000 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "and", 0x00000f0f, 0x000000ff, 0x0000000f ),
    gen_rr_src1_eq_dest_test( "and", 0x0000f0f0, 0x00000ff0, 0x000000f0 ),
    gen_rr_src0_eq_src1_test( "and", 0x000f0f00, 0x000f0f00 ),
    gen_rr_srcs_eq_dest_test( "and", 0x000f0f00, 0x000f0f00 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "and", 0xff00ff00, 0x0f0f0f0f, 0x0f000f00 ),
    gen_rr_value_test( "and", 0x0ff00ff0, 0xf0f0f0f0, 0x00f000f0 ),
    gen_rr_value_test( "and", 0x00ff00ff, 0x0f0f0f0f, 0x000f000f ),
    gen_rr_value_test( "and", 0xf00ff00f, 0xf0f0f0f0, 0xf000f000 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    dest = src0 & src1
    asm_code.append( gen_rr_value_test( "and", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "name,test", [
  asm_test( gen_basic_test     ),
  asm_test( gen_dest_byp_test  ),
  asm_test( gen_src0_byp_test  ),
  asm_test( gen_src1_byp_test  ),
  asm_test( gen_srcs_byp_test  ),
  asm_test( gen_srcs_dest_test ),
  asm_test( gen_value_test     ),
  asm_test( gen_random_test    ),
])
def test( name, test ):
  sim = PisaSim( trace_en=True )
  sim.load( pisa_encoding.assemble( test() ) )
  sim.run()

