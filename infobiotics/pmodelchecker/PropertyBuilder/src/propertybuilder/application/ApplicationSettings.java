
package propertybuilder.application;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import propertybuilder.application.data.Constant;
import propertybuilder.application.data.ConstantDataModel;
import propertybuilder.application.data.VariableDataModel;
import propertybuilder.pattern.Variable;
import propertybuilder.pattern.VariableType;

/**
 *
 * @author Ciprian
 */
public class ApplicationSettings {

    private ApplicationContext context;

    private String settingsFile = "config/settings.xml";
    private ArrayList<String> patternFiles;
    private ArrayList<String> invariantFiles;

    public boolean dumpOutputToFile;
    public boolean dumpOutputToStandardOutput;
    private String defaultPropertyFileName;
    private String defaultRewardsFileName;

    private AppParameter[] appParams;

    public ApplicationSettings( ApplicationContext ctx ) {
        if( ctx == null ) {
            throw new NullPointerException( "Context must not be null!" );
        }
        setApplicationContext( ctx );

        init();
    }

    public void init() {
        patternFiles = new ArrayList<String>();
        invariantFiles = new ArrayList<String>();

        dumpOutputToFile = true;
        dumpOutputToStandardOutput = false;

        initAppParams();
    }

    private void initAppParams() {
        appParams = new AppParameter[3];
        appParams[0] = new AppParameter( "-params", true );
        appParams[1] = new AppParameter( "-paramsFile", true );
        appParams[2] = new AppParameter( "-settings", true );
    }

    public void setApplicationContext( ApplicationContext ctx ) {
        this.context = ctx;
    }

    public ApplicationContext getApplicationContext() {
        return this.context;
    }

    public ArrayList<String> getPatternFiles() {
        return this.patternFiles;
    }

    public ArrayList<String> getInvariantFiles() {
        return this.invariantFiles;
    }

    public String getDefaultPropertyFileName() {
        return this.defaultPropertyFileName;
    }

    public String getDefaultRewardsFileName() {
        return this.defaultRewardsFileName;
    }

    public void setDefaultPropertyFileName( String dpfn ) {
        this.defaultPropertyFileName = dpfn;
    }

    public void setDefaultRewardsFileName( String drfn ) {
        this.defaultRewardsFileName = drfn;
    }

    public void getFromParams( String args[] ) {

        ArrayList<Document> settingsSources = new ArrayList<Document>();
        try {
            for ( int i = 0; i < appParams.length; i++ ) {
                appParams[i].processParameter( args );
            }
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            if ( appParams[1].isFound() ) {
                String value = appParams[1].getValue();
                if( value != null ) {
                    File f = new File( value );
                    if( f.exists() ) {
                        try {
                            settingsSources.add( db.parse( f ) );
                        } catch ( SAXException ex ) {
                            //display exception in log
                            ex.printStackTrace();
                        } catch ( IOException ex ) {
                            //display exception in log
                            ex.printStackTrace();
                        }
                    } else {
                        //display file not found int log
                    }
                }
            } 
            
            if ( appParams[2].isFound() ) {
                //either a file or direct xml input
                String value = appParams[2].getValue();
                if ( value != null ) {
                    //because "<" and ">" are not valid file characters
                    //this means we can check whether the parameter value is
                    //a filename or an xml specification of app params by simply
                    //detecting if the string starts with "<"
                    if ( value.startsWith( "<" ) ) {
                        try {
                            //value is XML
                            settingsSources.add( db.parse( new InputSource( new StringReader( value ) ) ) );
                        } catch ( SAXException ex ) {
                            //log error
                            ex.printStackTrace();
                        } catch ( IOException ex ) {
                            //log error
                            ex.printStackTrace();
                        }
                    } else {
                        //it must be a file
                        File f = new File( value );
                        if ( f.exists() ) {
                            try {
                                settingsSources.add( db.parse( f ) );
                            } catch ( SAXException ex ) {
                                //display exception in log
                                ex.printStackTrace();
                            } catch ( IOException ex ) {
                                //display exception in log
                                ex.printStackTrace();
                            }
                        } else {
                            //display file not found int log
                        }
                    }
                }
            }

            //if the params were entered directly to the command line in xml format
            if ( appParams[0].isFound() ) {
                String value = appParams[0].getValue();
                try {
                    settingsSources.add( db.parse( new InputSource( new StringReader( value ) ) ) );
                } catch ( SAXException ex ) {
                    //display exception in log
                    ex.printStackTrace();
                } catch ( IOException ex ) {
                    //display excetion in log
                    ex.printStackTrace();
                }
            }

            if ( settingsSources.size() == 0 ) {
                try {
                    //log in context that no settings were found and that we are attempting
                    //for the default settings file
                    settingsSources.add( db.parse( new File( settingsFile ) ) );
                } catch ( SAXException ex ) {
                    //log exception
                    ex.printStackTrace();
                } catch( FileNotFoundException ex ) {
                    ex.printStackTrace();
                } catch ( IOException ex ) {
                    //log exception
                    ex.printStackTrace();
                }
            }

        } catch ( ParserConfigurationException ex ) {
            ex.printStackTrace();
        }

        if( settingsSources.size() == 0 ) {
            //log no valid settings found
        } else {
            try {
                harvestSettingsSources( settingsSources );
            } catch ( XPathExpressionException ex ) {
                ex.printStackTrace();
            }
        }
    }

    private void harvestSettingsSources( List<Document> sources ) throws XPathExpressionException {

        VariableDataModel varData = context.getApplicationData().variableData;
        ConstantDataModel constantData = context.getApplicationData().constantData;
        XPathFactory xpf = XPathFactory.newInstance();
        XPath xp = xpf.newXPath();
        XPathExpression vexp = xp.compile( "/params/modelVariables/variable" );
        XPathExpression cexp = xp.compile( "/params/modelConstants/constant" );
        XPathExpression pexp = xp.compile( "/params/listOfPatternSources/patternFile" );        
        XPathExpression varIdExp = xp.compile( "@id" );
        XPathExpression varNameExp = xp.compile( "name/text()" );
        XPathExpression varDescriptionExp = xp.compile( "description/text()" );
        XPathExpression varTypeExp = xp.compile( "type/text()" );
        XPathExpression varValueExp = xp.compile( "value/text()" );
        XPathExpression patternSourceExp = xp.compile( "@src" );
        XPathExpression dtraceExp = xp.compile( "/params/dtrace/@src" );
        XPathExpression defaultPropFileExp = xp.compile( "/params/output/defaultPropertyFile/@value" );
        XPathExpression defaultRewardsFileExp = xp.compile( "/params/output/defaultRewardsFile/@value" );
        XPathExpression dumpOutputExp = xp.compile( "/params/output/dumpOutput" );
        
        Iterator<Document> it = sources.iterator();
        while( it.hasNext() ) {
            Document doc = it.next();
            NodeList varNodes = (NodeList) vexp.evaluate( doc, XPathConstants.NODESET );
            int length = varNodes.getLength();
            for( int i = 0; i < length; i++ ) {
                Node varNode = varNodes.item( i );
                String id = varIdExp.evaluate( varNode );
                String name = varNameExp.evaluate( varNode );
                String description = varDescriptionExp.evaluate( varNode );
                String type = varTypeExp.evaluate( varNode );
                varData.addVariable( new Variable( id, name, type, description ) );
            }

            NodeList constantNodes = (NodeList) cexp.evaluate( doc, XPathConstants.NODESET );
            length = constantNodes.getLength();
            for( int i = 0; i < length; i++ ) {
                Node constantNode = constantNodes.item( i );
                Constant constant = new Constant();
                constant.setId( varIdExp.evaluate( constantNode ) );
                constant.setName( varNameExp.evaluate( constantNode ) );
                constant.setDescription( varDescriptionExp.evaluate( constantNode ) );
                constant.setType( varTypeExp.evaluate( constantNode ) );
                constant.setValue( varValueExp.evaluate( constantNode ) );
                constantData.addConstant( constant );
            }

            NodeList patternNodes = (NodeList) pexp.evaluate( doc, XPathConstants.NODESET );
            length = patternNodes.getLength();
            for( int i = 0; i < length; i++ ) {
                Node patternNode = patternNodes.item( i );
                patternFiles.add( patternSourceExp.evaluate( patternNode ) );
            }

            String dtrace = dtraceExp.evaluate( doc );
            if( !dtrace.isEmpty() ) {
                invariantFiles.add( dtrace );
            }

            String dpf = defaultPropFileExp.evaluate( doc );
            if( !dpf.isEmpty() ) {
                defaultPropertyFileName = dpf;
            }

            String drf = defaultRewardsFileExp.evaluate( doc );
            if( !drf.isEmpty() ) {
                defaultRewardsFileName = drf;
            }   

            Node outputDumpNode = (Node) dumpOutputExp.evaluate( doc, XPathConstants.NODE );
            if( outputDumpNode != null ) {
                dumpOutputToFile = Boolean.valueOf( xp.evaluate( "@toFile", outputDumpNode ) );
                dumpOutputToStandardOutput = Boolean.valueOf( xp.evaluate( "@toStandardOutput", outputDumpNode ) );
            }
        }

        context.fireSettingsLoaded();
    }

    private void harvestSettingsSources( List<Document> sources, boolean resetSettings )
            throws XPathExpressionException {

        if( resetSettings ) {
            patternFiles.clear();
            invariantFiles.clear();

            dumpOutputToFile = true;
            dumpOutputToStandardOutput = false;
        }
        
        harvestSettingsSources( sources );
    }

    @Override
    public String toString() {
        StringBuffer buf = new StringBuffer();
        String lineSep = System.getProperty( "line.separator" );

        buf.append( "Settings: " + lineSep );
        buf.append( "Pattern files: [" );
        Iterator<String> it = patternFiles.iterator();
        while( it.hasNext() ) {
            buf.append( it.next() );
            buf.append( "; " );
        }
        buf.append( "]" + lineSep );
        buf.append( "Daikon trace files: [" );
        it = this.invariantFiles.iterator();
        while( it.hasNext() ) {
            buf.append( it.next() + "; " );
        }
        buf.append( "]" + lineSep );
        buf.append( "Default property filename: " );
        buf.append( defaultPropertyFileName + lineSep );
        buf.append( "Default rewards filename: " );
        buf.append( defaultRewardsFileName + lineSep );
        buf.append( "Dump to file: " );
        buf.append( String.valueOf( dumpOutputToFile ) );
        buf.append( lineSep );
        buf.append( "Dump to standard output: " );
        buf.append( String.valueOf( dumpOutputToStandardOutput ) );
        buf.append( lineSep );

        return buf.toString();
    }
}
