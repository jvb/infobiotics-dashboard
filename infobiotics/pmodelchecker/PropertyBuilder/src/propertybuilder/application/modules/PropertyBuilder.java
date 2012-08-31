
package propertybuilder.application.modules;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import javax.swing.BorderFactory;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import propertybuilder.application.AbstractCommandExecutor;
import propertybuilder.application.ApplicationContext;
import propertybuilder.application.ApplicationData;
import propertybuilder.application.ApplicationModule;
import propertybuilder.application.ArgumentList;
import propertybuilder.application.ContextListener;
import propertybuilder.application.VisibleApplicationModule;
import propertybuilder.application.data.PatternDataModel;
import propertybuilder.application.gui.ConstantJList;
import propertybuilder.application.gui.PatternCategoryCB;
import propertybuilder.application.gui.PatternJList;
import propertybuilder.application.gui.StateJList;
import propertybuilder.application.gui.VariableJList;
import propertybuilder.pattern.Pattern;
import propertybuilder.pattern.PatternType;

/**
 *
 * @author Ciprian
 */
public class PropertyBuilder extends AbstractCommandExecutor implements 
        VisibleApplicationModule, ContextListener {

    private String name = "Property Builder";
    private PropertyBuilderGUI gui;
    //local reference to the application data
    private ApplicationData appData;

    public PropertyBuilder() {
        gui = new PropertyBuilderGUI();
    }

    public void init( ApplicationContext context ) {
        context.getGUI().addModuleComponent( this );
    }

    public void dispose() {
        System.out.println( "Dispose Property Builder" );
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
        context.addContextListener( this );
    }

    // <editor-fold defaultstate="collapsed" desc="ContextListener methods">
    public void settingsLoaded() {
        
    }

    public void patternsLoaded() {
        PatternDataModel model = appData.patternRepository.getModel( PatternType.PROPERTY, true );
        gui.propertyPatternList.setModel( model.asListModel() );
        gui.patterncb.setModel( model.patternClassModel() );
        SwingUtilities.updateComponentTreeUI( gui );
    }

    public void patternDataChanged() {
        
    }

    public void patternSelected( Pattern p ) {
        if( p.getType() == PatternType.PROPERTY ) {
            
        }
    }
    // </editor-fold>

    private class PropertyBuilderGUI extends JPanel {

        protected PatternJList recentlyUsedList;
        protected PatternJList propertyPatternList;
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
        private Color componentForeground = new Color( 38, 88, 138 );

        public PropertyBuilderGUI() {
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

            Pattern p = new Pattern();
            p.setName( "Property pattern 1" );
            p.setId( "PropP1" );
            p.setDescription( "This is a demo PROPERTY pattern to test the display method" );
            p.setPatternClass( "State pattern class1" );
            p.setPatternType( PatternType.PROPERTY );
            p.setQuestion( "A state [s] persists indefinitely." );

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
            stateResultta.setText( "Property formula goes here (ex: P=? [ (x > 0) U true ]" );
            extractPatternInfo( p );

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

            aux2 = new JPanel( new FlowLayout( FlowLayout.LEADING ) );
            aux2.add(  new JLabel( "A state " ) );
            aux2.add(  new JComboBox( new String[] { "state1", "state2", "state3" } ) );
            aux2.add(  new JLabel( " persists indefinitely." ) );
            aux1.add(  aux2, BorderLayout.CENTER );

            constructionPanel.add( aux1, BorderLayout.CENTER );

            //set up the states panel
            String[] tempStates = new String[40];
            for( int i = 0; i < tempStates.length; i++ ) {
                tempStates[i] = "Property " + i;
            }

            stateList = new StateJList( tempStates );
            JScrollPane listContainer = new JScrollPane( stateList );
            listContainer.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Properties" ) );
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

            JSplitPane sp = new JSplitPane( JSplitPane.VERTICAL_SPLIT );
            panel.add( sp );

            String[] recentlyUsed = new String[50];
            for( int i = 0; i < recentlyUsed.length; i++ ) {
                recentlyUsed[i] = "recently used" + i;
            }
            recentlyUsedList = new PatternJList( recentlyUsed );
            recentlyUsedList.setFixedCellWidth( 200 );
            JScrollPane scrollpane = new JScrollPane( recentlyUsedList );
            scrollpane.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Recently used" ) );
            sp.setTopComponent( scrollpane );

            String[] tempPatterns = new String[50];
            for( int i = 0; i < tempPatterns.length; i++ ) {
                tempPatterns[i] = "pattern" + i;
            }

            propertyPatternList = new PatternJList( tempPatterns);
            scrollpane = new JScrollPane( propertyPatternList );
            scrollpane.setBorder( BorderFactory.createEtchedBorder() );
            JPanel lowerPanel = new JPanel( new BorderLayout() );
            lowerPanel.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Pattern select" ) );

            JPanel ltop = new JPanel( new BorderLayout() );
            ltop.add( new JLabel( "Pattern class: " ), BorderLayout.NORTH );

            String[] pclasses = new String[] { "class 1", "class2", "class3" };
            patterncb = new PatternCategoryCB( pclasses );
            ltop.add( patterncb, BorderLayout.SOUTH );

            lowerPanel.add( ltop, BorderLayout.NORTH );
            lowerPanel.add( scrollpane, BorderLayout.CENTER );

            sp.setBottomComponent( lowerPanel );

            return panel;
        }

        private JPanel makeRightPanel() {
            JPanel panel = new JPanel( new BorderLayout() );

            JSplitPane sp = new JSplitPane( JSplitPane.VERTICAL_SPLIT );
            panel.add( sp );

            String[] vars = new String[] { "v1", "v2", "v3", "state1", "state2", "state3" };
            variableList = new VariableJList( vars );
            variableList.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Variables" ) );
            sp.setTopComponent( variableList );
            sp.setDividerLocation( 300 );

            String[] constants = new String[] { "const_01 : 50", "const_02 : 80", "const_03 : 0", "const_04 : 150", "const_05 : 500" };
            constantList = new ConstantJList( constants);
            constantList.setBorder( BorderFactory.createTitledBorder( BorderFactory.createEtchedBorder(), "Constants" ) );
            sp.setBottomComponent( constantList );

            return panel;
        }
    }
}
