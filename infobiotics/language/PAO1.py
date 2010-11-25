''' 

Determinstic rates:
    1. Distinguish from stochastic rates
    2. Convert deterministic rates to stochastic rates if stochastic rate not given, with warning.
    

'''

from infobiotics.language import *


# Jonathan Blakes 20101022 #

# lecA transcriptional and post-transcriptional regulation in PAO1 #

# Constants were adapted from Brown 2010 using Wilkinson p.169 #
# in brown_constants.txt #

# Model does not contain GacA or GacS, RsmE (not in PAO1) or RsmX #

# Compartment bacterium is inside medium allowing population density to be # 
# tuned by rate of diffusion between media #

# PQS production is maximal and uncontrolled #


# Jonathan Blakes 20101103 #

# 1 Create Brown model as a module with known constants #
#       due to disparity between ODE and P systems there are more rules than constants #
# 2 Add our model with PQS a second module with tunable constants #


class Brown(compartment):
    # Even though PAO1 does not have the rsmX gene Brown says in Table 1 
    # footnote a that the dynamics of RsmY are the same as for RsmX so I have #
    # used the constants for RsmX for RsmY #
    
    r000 = reaction('gacS -> gacS + GacS g_S0=60.221415 # "Basal GacS synthesis" (example compressed rule)', reactants_label='bacteria', products_label='bacteria')
    # GacS synthesis #
    r001 = reaction('[ gacS ] -g_S0-> [ gacS + GacS ]                 g_S0=60.221415        # "Basal GacS synthesis" #', reactants_label='bacteria', products_label='bacteria')
    r002 = '[ GacA_gacS ] -g_SA2-> [ GacA_gacS + GacS ]         g_SA2=300             # roughly half maximal synthesis 602.21415 #' 
    r003 = '[ GacAx2_gacS ] -g_SA-> [ GacAx2_gacS + GacS ]     g_SA=602.21415         # Maximum GacS synthesis #'
    
    # cooperative binding of GacA to gacS #            
    r004 = '[ GacA + gacS ] -c_on-> [ GacA_gacS ]                 c_on=11.9558798145'
    r005 = '[ GacA_gacS ] -K_SA_off-> [ GacA + gacS ]             K_SA_off=1440.0'
    r006 = '[ GacA + GacA_gacS ] -c_on-> [ GacAx2_gacS ]         c_on=11.9558798145'
    r007 = '[ GacAx2_gacS ] -K_SA_off2-> [ GacA + GacA_gacS ]     K_SA_off2=1220.0     # 1440.0 divided by the Hill coefficient h_A of 2 #'            
    
    # cooperative binding of signal to GacS #
    r008 = '[ signal + GacS ] -c_on-> [ signal_GacS ]                 c_on    =11.9558798145'
    r009 = '[ signal_GacS ] -K_S_off-> [ signal + GacS ]             K_S_off    =57.6'
    r010 = '[ signal + signal_GacS ] -c_on-> [ signalx2_GacS ]         c_on    =11.9558798145'
    r011 = '[ signalx2_GacS ] -K_S_off2-> [ signal + signal_GacS ]     K_S_off2=28.8         # 57.6 divided by the Hill coefficient h_Q of 2 #' 
    
    # phosphorylation of GacS #
    r012 = '[ signalx2_GacS ] -k_plusS-> [ signalx2_GacS_P ]     k_plusS    =100     # autophosphorylation of GacS - what happens to signal now - can we assume it stays bound #'
    r013 = '[ signalx2_GacS_P ] -k_D-> [ signalx2_GacS + P ]         k_D        =90        # GacS dephosphoryation - can use P as measure of how often this occurs since it is assumed to be in abundance #'

    # "In the presence of signal, GacS undergoes autophosphorylation and subsequently phosphorylated GacA." - Brown p201 2. Biological system #
    # Phosphorylation of GacA by GacS # 
    r014 = '[ signalx2_GacS_P + GacA ] -k_plusP-> [ signalx2_GacS + GacA_P ]     k_plusP=0.415134715782'
    r015 = '[ signalx2_GacS + GacA_P ] -k_minusP-> [ signalx2_GacS_P + GacA ]     k_minusP=0.332107772625'
    
    r016 = '[ GacS ] -m_S-> [  ]        m_S=1.5        # Decay of GacS # '
    
    r017 = '[ gacA ] -g_A-> [ gacA + GacA ]    g_A=10    # GacA synthesis #'
    r018 = '[ GacA ] -m_A-> [  ]                m_A=1    # GacA decay #'

    r019 = '[ Repressor + rsmY ] -c_on-> [ Repressor_rsmY ] c_on=11.9558798145'            
    r020 = '[ Repressor_rsmY ] -K_XI_off-> [ Repressor + rsmY ] K_XI_off=36.0  '  
    r021 = '[ Repressor + Repressor_rsmY ] -c_on-> [ Repressorx2_rsmY ] c_on=11.9558798145'            
    r022 = '[ Repressorx2_rsmY ] -K_XI_off2-> [ Repressor + Repressor_rsmY ] K_XI_off2=18.0 # h_I #'    

    r023 = '[ Repressor + rsmZ ] -c_on-> [ Repressor_rsmZ ] c_on=11.9558798145'            
    r024 = '[ Repressor_rsmZ ] -K_ZI_off-> [ Repressor + rsmZ ] K_ZI_off=36.0  '  
    r025 = '[ Repressor + Repressor_rsmZ ] -c_on-> [ Repressorx2_rsmZ ] c_on=11.9558798145'            
    r026 = '[ Repressorx2_rsmZ ] -K_ZI_off2-> [ Repressor + Repressor_rsmZ ] K_ZI_off2=18.0 # h_I #'    

    r027 = '[ rsmY ] -g_X0-> [ rsmY + RsmY ] g_X0=0'
    
    r028 = '[ rsmZ ] -g_Z0-> [ rsmZ + RsmZ ] g_Z0=0'
    
    r029 = '[ GacA + rsmY ] -c_on-> [ GacA_rsmY ] c_on=11.9558798145'            
    r030 = '[ GacA_rsmY ] -K_XA_off-> [ GacA + rsmY ] K_XA_off=720.0'
    r031 = '[ GacA + GacA_rsmY ] -c_on-> [ GacAx2_rsmY ] c_on=11.9558798145'            
    r032 = '[ GacAx2_rsmY ] -K_XA_off2-> [ GacA + GacA_rsmY ] K_XA_off2=360    # h_A #'

    r033 = '[ GacA + rsmZ ] -c_on-> [ GacA_rsmZ ] c_on=11.9558798145'
    r034 = '[ GacA_rsmZ ] -K_ZA_off-> [ GacA + rsmZ ] K_ZA_off=1440.0'
    r035 = '[ GacA + GacA_rsmZ ] -c_on-> [ GacAx2_rsmZ ] c_on=11.9558798145'            
    r036 = '[ GacAx2_rsmZ ] -K_ZA_off2-> [ GacA + GacA_rsmZ ] K_ZA_off2=720    # h_A #'

    r037 = '[ GacAx2_rsmY ] -g_XA-> [ GacAx2_rsmY + rsmY ] g_XA=2005.3731195 # Maximum RsmY synthesis #'
    r038 = '[ GacAx2_rsmZ ] -g_ZA-> [ GacAx2_rsmZ + rsmZ ] g_ZA=1005.6976305 # Maximum RsmZ synthesis #'

    
    # We known that 1 RsmZ/RsmY can sequester up to 5 RsmA although Brown assumes RsmZ 1 = 4 RsmA #
    # He also assumes non-cooperativity #
    
    r039 = '[ RsmZ + RsmA ] -k_plusRZ-> [ RsmZ_RsmA ]            k_plusRZ=0.0232475440838    # 1st binding #'
    r040 = '[ RsmZ_RsmA + RsmA ] -k_plusRZ-> [ RsmZ_RsmAx2 ]     k_plusRZ=0.0232475440838    # 2nd binding #'
    r041 = '[ RsmZ_RsmAx2 + RsmA ] -k_plusRZ-> [ RsmZ_RsmAx3 ]   k_plusRZ=0.0232475440838    # 3rd binding #'
    r042 = '[ RsmZ_RsmAx3 + RsmA ] -k_plusRZ-> [ RsmZ_RsmAx4 ]   k_plusRZ=0.0232475440838    # 4th binding #'
    r043 = '[ RsmZ_RsmAx4 + RsmA ] -k_plusRZ-> [ RsmZ_RsmAx5 ]   k_plusRZ=0.0232475440838    # 5th binding #'
    r044 = '[ RsmZ_RsmAx5 ] -k_minusRZ-> [ RsmZ_RsmAx4 + RsmA ]  k_minusRZ=1                 # 1st debinding #'
    r045 = '[ RsmZ_RsmAx4 ] -k_minusRZ-> [ RsmZ_RsmAx3 + RsmA ]  k_minusRZ=1                 # 2nd debinding #'
    r046 = '[ RsmZ_RsmAx3 ] -k_minusRZ-> [ RsmZ_RsmAx2 + RsmA ]  k_minusRZ=1                 # 3rd debinding #'
    r047 = '[ RsmZ_RsmAx2 ] -k_minusRZ-> [ RsmZ_RsmA + RsmA ]    k_minusRZ=1                 # 4th debinding #'
    r048 = '[ RsmZ_RsmA ] -k_minusRZ-> [ RsmZ + RsmA ]           k_minusRZ=1                 # 5th debinding #'
    r049 = '[ RsmZ_RsmA ] -m_RZ-> [  ]                           m_RZ=1.5'
    r050 = '[ RsmZ_RsmAx2 ] -m_RZ-> [  ]                         m_RZ=1.5'
    r051 = '[ RsmZ_RsmAx3 ] -m_RZ-> [  ]                         m_RZ=1.5'
    r052 = '[ RsmZ_RsmAx4 ] -m_RZ-> [  ]                         m_RZ=1.5'
    r053 = '[ RsmZ_RsmAx5 ] -m_RZ-> [  ]                         m_RZ=1.5'

    r054 = '[ RsmY + RsmA ] -k_plusRX-> [ RsmY_RsmA ]            k_plusRX=0.0232475440838    # 1st binding #'
    r055 = '[ RsmY_RsmA + RsmA ] -k_plusRX-> [ RsmY_RsmAx2 ]     k_plusRX=0.0232475440838    # 2nd binding #'
    r056 = '[ RsmY_RsmAx2 + RsmA ] -k_plusRX-> [ RsmY_RsmAx3 ]   k_plusRX=0.0232475440838    # 3rd binding #'
    r057 = '[ RsmY_RsmAx3 + RsmA ] -k_plusRX-> [ RsmY_RsmAx4 ]   k_plusRX=0.0232475440838    # 4th binding #'
    r058 = '[ RsmY_RsmAx4 + RsmA ] -k_plusRX-> [ RsmY_RsmAx5 ]   k_plusRX=0.0232475440838    # 5th binding #'
    r059 = '[ RsmY_RsmAx5 ] -k_minusRX-> [ RsmY_RsmAx4 + RsmA ]  k_minusRX=1                 # 1st debinding #'
    r060 = '[ RsmY_RsmAx4 ] -k_minusRX-> [ RsmY_RsmAx3 + RsmA ]  k_minusRX=1                 # 2nd debinding #'
    r061 = '[ RsmY_RsmAx3 ] -k_minusRX-> [ RsmY_RsmAx2 + RsmA ]  k_minusRX=1                 # 3rd debinding #'
    r062 = '[ RsmY_RsmAx2 ] -k_minusRX-> [ RsmY_RsmA + RsmA ]    k_minusRX=1                 # 4th debinding #'
    r063 = '[ RsmY_RsmA ] -k_minusRX-> [ RsmY + RsmA ]           k_minusRX=1                 # 5th debinding #'
    r064 = '[ RsmY_RsmA ] -m_RX-> [  ]                           m_RX=1.5'
    r065 = '[ RsmY_RsmAx2 ] -m_RX-> [  ]                         m_RX=1.5'
    r066 = '[ RsmY_RsmAx3 ] -m_RX-> [  ]                         m_RX=1.5'
    r067 = '[ RsmY_RsmAx4 ] -m_RX-> [  ]                         m_RX=1.5'
    r068 = '[ RsmY_RsmAx5 ] -m_RX-> [  ]                         m_RX=1.5'

    r069 = '[ RsmY ] -m_X-> [ ]  m_X=15  # RsmY decay #'
    r070 = '[ RsmZ ] -m_Z-> [ ]  m_Z=7   # RsmZ decay #'

    
    r071 = '[ Repressor_producer ] -g_I-> [ Repressor_producer + Repressor ] g_I=301.107075 # Maximum repressor synthesis #'
    
    # RsmA represses Repressor synthesis #
    r072 = '[ RsmA + Repressor ] -K_IR_on-> [ RsmA_Repressor ] K_IR_on = 11.9558798145'
    r073 = '[ RsmA_Repressor ] -K_IR_off-> [ RsmA + Repressor ] K_IR_off = 36.0'
    
    r074 = '[ Repressor ] -m_I-> [  ] m_I=3.0 # Repressor decay #'
    
    # RsmA binds signal mRNA # 
    r075 = '[ signal_producer ] -g_Q-> [ signal_producer + signal ]  g_Q=72265.698  # maximal synthesis of GacS activating signal (very high - slows simulation considerably) #'
    
    
    r076 = '[ signal ] -m_Q-> [ ]                                      m_Q=10         # intracellular signal decay #'
    r077 = '[ signal ] -d-> signal [ ]                                  d=100           # signal diffusion #'
        


class Blakes(compartment):

    r101 = '[ PqsH ]_l -c_PQS_synthesis-> [ PqsH + PQS ]_l      kkk=0         # PQS synthesis by PqsH (PqsH is the final product of the pqs operon) #' 
    r102 = '[ PQS ]_l -c_PQS_decay-> [ ]_l                      kkk=0         # intracellular PQS decay #'
    r103 = '[ PQS ]_l -c_PQS_diffusion_out-> PQS [  ]_l              kkk=0       # PQS diffusion out of the compartment (opposite rule in medium - does not work the other way round) #'

    # RsmA synthesis and decay #
    r104 = '[ rsmA_repressed ]_l -x-> [ rsmA ]_l             x = 1            # artificial delay in rsmA availability #'
    r105 = '    r9: [ rsmA ]_l -g_R-> [ rsmA + RsmA ]_l              g_R = 180.664245 # transcription and translation in one #'
    r106 = '    r10: [ RsmA ]_l -m_R-> [ ]_l                         m_R = 1.0        # decay of protein #'
    
    # RsmZ synthesis - controlled by PQS (actually GacA - maybe slower than with lecA) - and decay # 
    r107 = 'r13: [ PQS + rsmZ ]_l -K_Son-> [ PQS_rsmZ ]_l        K_Son = 1            # binding #'
    r108 = 'r14: [ PQS_rsmZ ]_l -K_Soff-> [ PQS + rsmZ ]_l       K_Soff = 125         # debinding #'
    r109 = 'r: [ PQS_rsmZ ]_l -g_ZA-> [ PQS_rsmZ + RsmZ ]_l    g_ZA = 1005.6976305  # RsmZ is an mRNA #'
    
    # lecA synthesis controlled by PQS (maybe quicker than with rsmZ) # 
    r110 = 'r32: [ PQS + lecA ]_l -K_Son-> [ PQS_lecA ]_l               K_Son = 1             # PQS binding lecA #'
    r111 = 'r33: [ PQS_lecA ]_l -K_Soff-> [ PQS + lecA ]_l              K_Soff = 125          # PQS_lecA debinding #'
    r112 = 'r34: [ PQS_lecA ]_l -doubleg_ZA-> [ PQS_lecA + mLecA ]_l    doubleg_ZA = 2010     # lecA transcription #'
    r113 = 'r35: [ mLecA ]_l -m_Z-> [ ]_l                               m_Z = 7               # mLecA transcript decay #'
    r114 = 'r36: [ mLecA ]_l -doubleg_ZA-> [ LecA ]_l                   doubleg_ZA = 2010     # mLecA translation - LecA production #'
    r115 = 'r37: [ LecA ]_l -m_Z-> [ ]_l                                m_Z = 7               # LecA decay #'

    # 1 RsmA can sequester 1 mLecA - maybe weaker than RsmZ binding RsmA (or RsmA binding RsmZ depending on how you look at it) #
    r116 = 'r38: [ RsmA + mLecA ]_l -K_ZAon-> [ RsmA_mLecA ]_l   K_ZAon = 1'   
    r117 = 'r39: [ RsmA_mLecA ]_l -K_ZAoff-> [ RsmA + mLecA ]_l  K_ZAoff = 5'


def blakes():
    return Blakes

class bacteria(Brown, blakes()): # using multiple inheritance for modularity
    rsmA_repressed = 1
    PqsH = 30
    rsmZ = 1
    lecA = 1
    


class media(compartment):
    bacteria = bacteria()
    
#    r201 = '[PQS] -> [ ] m_QE=10'
#    r202 = '[ PQS ]_medium=( 1, 0)=[  ] -d-> [  ]_medium=( 1, 0)=[ PQS ]  d=100'
#    r203 = '[ PQS ]_medium=(-1, 0)=[  ] -d-> [  ]_medium=(-1, 0)=[ PQS ]  d=100'
#    r204 = '[ PQS ]_medium=( 0, 1)=[  ] -d-> [  ]_medium=( 0, 1)=[ PQS ]  d=100'
#    r205 = '[ PQS ]_medium=( 0,-1)=[  ] -d-> [  ]_medium=( 0,-1)=[ PQS ]  d=100'
#    r206 = 'PQS [ ]_bacterium -d-> [ PQS ]_bacterium    d=100'
    
#    _d = 100
#    r200 = reaction('[ PQS ]_medium=( 0,-1)=[  ] -d-> [  ]_medium=( 0,-1)=[ PQS ]  d=100', stochastic_rate_constant=_d)
    r200 = reaction('[ PQS ]_medium=( 0,-1)=[  ] -100.0-> [  ]_medium=( 0,-1)=[ PQS ]')

#m = model([[rsmAKnockout(name='rsmA', _x=x, _y=y) if (x == 4 and y == 4) else WildType(name='wt', _x=x, _y=y) for x in range(10)] for y in range(10)])
#m = model([[media(_x=x, _y=y) for x in range(1)] for y in range(1)])
m = model(
    [
        [
            media(
                _x=x,
                _y=y,
            ) 
            for x in range(1)
        ] 
        for y in range(1)
    ]
)

## evalable!
#a = eval("""model(
#    [
#        [
#            compartment(
#                bacteria(),
#                label='media',
#                _x=x,
#                _y=y,
#            ) 
#            for x in range(1)
#        ] 
#        for y in range(1)
#    ]
#)""")
#print a


media = m.distribution[0, 0]

#print media.label

#print media.outside


b = media.bacteria

#print bacteria.label

#print b.outside #TODO return label not <class 'infobiotics.language.metacompartment.metacompartment'>

#for s in b.species:
#    print s.str()

for r in b.reactions:
    print r.str(comment=True)



