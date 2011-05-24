
package propertybuilder.application.modules;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.Iterator;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import propertybuilder.application.AbstractCommandExecutor;
import propertybuilder.application.ApplicationContext;
import propertybuilder.application.ApplicationData;
import propertybuilder.application.ApplicationModule;
import propertybuilder.application.ArgumentList;
import propertybuilder.application.ContextListener;
import propertybuilder.application.VisibleApplicationModule;
import propertybuilder.application.aspects.SymbolSubstituteFactory;
import propertybuilder.application.data.PatternDataModel;
import propertybuilder.application.gui.ConstantJList;
import propertybuilder.application.gui.PatternCategoryCB;
import propertybuilder.application.gui.PatternJList;
import propertybuilder.application.gui.StateJList;
import propertybuilder.application.gui.VariableJList;
import propertybuilder.pattern.Pattern;
import propertybuilder.pattern.PatternType;
import propertybuilder.pattern.Symbol;

/**
 *
 * @author Ciprian
 */
public class StateBuilder extends AbstractCommandExecutor implements 
        VisibleApplicationModule, ContextListener {

    private String name = "State Builder";
    private StateBuilderGUI gui;
    private ApplicationData appData;

    //local reference to application context
    private ApplicationContext ctx;
    private SymbolSubstituteFactory ssFactory;

    public StateBuilder() {
        gui = new StateBuilderGUI();
    }

    public void init( ApplicationContext context ) {
        context.getGUI().addModuleComponent( this );
    }

    public void dispose() {
        
    }

    public String getName() {
        return this.name;
    }

    public JComponent getGUI() {
        return this.gui;
    }

    public void execute( String cmd, ArgumentList args ) {
        
    }

    public void setModuleVisible( boolean b ) {
        gui.setVisible( b );
    }

    public void onInsert( ApplicationContext context ) {
        this.appData = context.getApplicationData();
        this.ctx = context;
        this.ssFactory = this.ctx.getApplicationUtilities().ssFactory;
        context.addContextListener( this );
    }

    // <editor-fold defaultstate="collapsed" desc="ContextListener methods">
    public void settingsLoaded() {
        gui.variableList.setModel( appData.variableData.getVariableListModel() );
        gui.constantList.setModel( appData.constantData.getConstantListModel() );
        SwingUtilities.updateComponentTreeUI( gui );
    }

    public void patternsLoaded() {
        PatternDataModel model = appData.patternRepository.getModel( PatternType.STATE, true );
        gui.statePatternList.setModel( model.asListModel() );
        gui.patterncb.setModel( model.patternClassModel() );
        SwingUtilities.updateComponentTreeUI( gui );
    }

    public void patternDataChanged() {

    }

    public void patternSelected( Pattern p ) {
        if( p.getType() == PatternType.STATE ) {
            gui.selectedPatternName.setText( p.getName() );
            gui.selectedPatternId.setText( p.getId() );
            gui.selectedPatternQuestion.setText( p.getQuestion() );
            gui.selectedPatternClass.setText( p.getPatternClass() );
            gui.selectedPatternDescription.setText( p.getDescription() );

            Component[] components = gui.symbolPanel.getComponents();
            for( int i = 0; i < components.length; i++ ) {
                if( components[i] instanceof JComponent ) {
                    ssFactory.releaseSubstitute( (JComponent) components[i] );
                }
            }
            gui.symbolPanel.removeAll();

            Iterator<Symbol> it = p.getTemplate().iterator();
            while( it.hasNext() ) {
                gui.symbolPanel.add( ssFactory.getSubstitute( it.next() ) );
            }
            gui.symbolPanel.setPreferredSize(gui.symbolPanel.getMinimumSize());
        }
    }
    // </editor-fold>

    private class StateBuilderGUI extends JPanel {

        protected PatternJList recentlyUsedList;
        protected PatternJList statePatternList;
        protected VariableJList variableList;
        protected ConstantJList constantList;
        protected PatternCategoryCB patterncb;
        protected StateJList stateList;

        protected JLabel selectedPatternName;
        protected JLabel selectedPatternClass;
        protected JTextArea selectedPatternDescription;
        protected JLabel selectedPatternId;
        protected JLabel selectedPatternQuestion;
        protected JTextArea stateResultta;
        protected JButton addStateButton;
        protected JButton removeStateButton;
        protected JButton clearStatesButton;
        private Color componentForeground = new Color( 38, 88, 138 );
        protected JPanel symbolPanel;

        public StateBuilderGUI() {
            super( new BorderLayout());

            JSplitPane sp1 = new JSplitPane( JSplitPane.HORIZONTAL_SPLIT );
            sp1.setLeftComponent( makeLeftPanel() );

            JSplitPane sp2 = new JSplitPane( JSplitPane.HORIZONTAL_SPLIT );
            sp2.setLeftComponent( makeCentrePanel() );
            sp2.setRightComponent( makeRightPanel() );
            sp2.setDividerLocation( 550 );

            sp1.setRightComponent( sp2 );
            this.add( sp1, BorderLayout.CENTER );
        }

        private JPanel makeCentrePanel() {
            JPanel panel = new JPanel( new BorderLayout() );

            JSplitPane sp = new JSplitPane( JSplitPane.VERTICAL_SPLIT );

            //Set up the construction panel
            JPanel constructionPanel = new JPanel( new BorderLayout() );
            sp.setTopComponent( constructionPanel );

            //first init all components that will fit here;
            selectedPatternName = new JLabel( "" );
            selectedPatternName.setForeground( componentForeground );
            selectedPatternId = new JLabel( "" );
            selectedPatternId.setForeground( componentForeground );
            selectedPatternClass = new JLabel( "" );
            selectedPatternClass.setForeground( componentForeground );
            selectedPatternDescription = new JTextArea( 3, 20 );
            selectedPatternDescription.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Description" ) );
            selectedPatternDescription.setEditable( false );
            selectedPatternDescription.setForeground( componentForeground );
            selectedPatternQuestion = new JLabel( "" );
            selectedPatternQuestion.setForeground( componentForeground );
            stateResultta = new JTextArea( 3, 20 );
            stateResultta.setForeground( componentForeground );

            JPanel aux1 = new JPanel( new BorderLayout() );
            aux1.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Pattern Details" ) );
            JPanel aux2 = new JPanel( new FlowLayout( FlowLayout.LEADING ) );
            aux2.add( new JLabel( "Pattern: " ) );
            aux2.add( selectedPatternName );
            aux2.add(  new JLabel( "ID: " ) );
            aux2.add(  selectedPatternId );

            aux1.add( aux2, BorderLayout.NORTH );
            aux1.add( selectedPatternDescription, BorderLayout.CENTER );
            constructionPanel.add( aux1, BorderLayout.NORTH );

            aux1 = new JPanel( new BorderLayout() );
            aux1.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Builder" ) );
            JPanel templatePanel = new JPanel( new FlowLayout( FlowLayout.LEADING ) );
            templatePanel.add(  new JLabel( "Template: " ) );
            templatePanel.add( selectedPatternQuestion );
            aux1.add(  templatePanel, BorderLayout.NORTH );
            aux1.add( stateResultta, BorderLayout.SOUTH );

            symbolPanel = new JPanel( new FlowLayout( FlowLayout.LEADING ) );
            aux1.add( symbolPanel, BorderLayout.CENTER );

            JPanel aux3 = new JPanel( new FlowLayout( FlowLayout.TRAILING ) );
            addStateButton = new JButton( "Add State" );
            removeStateButton = new JButton( "Remove State" );
            clearStatesButton = new JButton( "Clear States" );
            aux3.add( addStateButton );
            aux3.add( removeStateButton );
            aux3.add( clearStatesButton );

            constructionPanel.add( aux1, BorderLayout.CENTER );
            constructionPanel.add( aux3, BorderLayout.SOUTH );

            //set up the states panel
            String[] tempStates = new String[40];
            for( int i = 0; i < tempStates.length; i++ ) {
                tempStates[i] = "State " + i;
            }

            stateList = new StateJList( tempStates );
            JScrollPane listContainer = new JScrollPane( stateList );
            listContainer.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "States" ) );
            sp.setBottomComponent( listContainer );

            panel.add( sp );

            return panel;
        }

        public void extractPatternInfo( Pattern pattern ) {
            if( pattern.getType() != PatternType.STATE ) {
                //execute a command on the context that will notify the user about this
            }
            
            selectedPatternName.setText( pattern.getName() );
            selectedPatternClass.setText( pattern.getPatternClass() );
            selectedPatternId.setText( pattern.getId() );
            selectedPatternDescription.setText( pattern.getDescription() );
            selectedPatternQuestion.setText( pattern.getQuestion() );
        }

        private JPanel makeLeftPanel() {
            JPanel panel = new JPanel( new BorderLayout() );
            panel.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Patterns" ) );

            String[] tempPatterns = new String[50];
            for( int i = 0; i < tempPatterns.length; i++ ) {
                tempPatterns[i] = "pattern" + i;
            }
            
            statePatternList = new PatternJList( tempPatterns);
            statePatternList.addListSelectionListener( new ListSelectionListener() {

                public void valueChanged( ListSelectionEvent e ) {
                    if( !e.getValueIsAdjusting() ) {
                        Object o = statePatternList.getSelectedValue();
                        if( o instanceof Pattern ) {
                            ctx.firePatternSelected( (Pattern) o );
                        }
                    }
                }

            });
            JScrollPane scrollpane = new JScrollPane( statePatternList );
            scrollpane.setBorder( BorderFactory.createEtchedBorder() );

            JPanel ltop = new JPanel( new BorderLayout() );
            ltop.add( new JLabel( "Pattern class: " ), BorderLayout.NORTH );

            patterncb = new PatternCategoryCB();
            patterncb.addItemListener( new ItemListener() {

                public void itemStateChanged( ItemEvent e ) {
                    if( e.getStateChange() == ItemEvent.SELECTED ) {
                        SwingUtilities.updateComponentTreeUI( statePatternList );
                    }
                }
                
            });
            ltop.add( patterncb, BorderLayout.SOUTH );

            panel.add(ltop, BorderLayout.NORTH);
            panel.add(scrollpane, BorderLayout.CENTER);

            return panel;
        }

        private JPanel makeRightPanel() {
            JPanel panel = new JPanel( new BorderLayout() );

            JSplitPane sp = new JSplitPane( JSplitPane.VERTICAL_SPLIT );
            panel.add( sp );

            variableList = new VariableJList();
            variableList.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Variables" ) );
            sp.setTopComponent( variableList );
            sp.setDividerLocation( 300 );

            constantList = new ConstantJList();
            constantList.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Constants" ) );
            sp.setBottomComponent( constantList );

            return panel;
        }
    }

}
