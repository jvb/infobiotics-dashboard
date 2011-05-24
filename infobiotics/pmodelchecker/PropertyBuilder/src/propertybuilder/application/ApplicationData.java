
package propertybuilder.application;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPathExpressionException;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;
import propertybuilder.application.data.ConstantDataModel;
import propertybuilder.application.data.DefaultConstantDataModel;
import propertybuilder.application.data.DefaultPropertyDataModel;
import propertybuilder.application.data.DefaultRewardsDataModel;
import propertybuilder.application.data.DefaultStateDataModel;
import propertybuilder.application.data.DefaultVariableDataModel;
import propertybuilder.application.data.PatternRepository;
import propertybuilder.application.data.PropertyDataModel;
import propertybuilder.application.data.RewardsDataModel;
import propertybuilder.application.data.StateDataModel;
import propertybuilder.application.data.VariableDataModel;
import propertybuilder.pattern.Pattern;
import propertybuilder.pattern.PatternType;

/**
 *
 * @author Ciprian
 */
public class ApplicationData implements ContextListener {

    private ApplicationContext context;

    public VariableDataModel variableData;
    public ConstantDataModel constantData;
    public StateDataModel stateData;
    public PropertyDataModel propertyData;
    public RewardsDataModel rewardsData;
    public PatternRepository patternRepository;
    public Hashtable<PatternType, Pattern> selectedPatterns;

    public ApplicationData( ApplicationContext ctx ) {
        if( ctx == null ) {
            throw new NullPointerException( "Context must not be null!" );
        }

        this.setApplicationContext( ctx );
        
        init();
    }

    public void init() {
        variableData = new DefaultVariableDataModel();
        constantData = new DefaultConstantDataModel();
        stateData = new DefaultStateDataModel();
        rewardsData = new DefaultRewardsDataModel();
        propertyData = new DefaultPropertyDataModel();
        patternRepository = new PatternRepository( this.context );
        selectedPatterns = new Hashtable<PatternType, Pattern>();
    }

    public void setApplicationContext( ApplicationContext ctx ) {
        this.context = ctx;
        context.addContextListener( this );
    }

    public ApplicationContext getApplicationContext() {
        return this.context;
    }
    // <editor-fold defaultstate="collapsed" desc="ContextListener methods">
    public void settingsLoaded() {
        ArrayList<String> patternFiles =
                this.context.getApplicationSettings().getPatternFiles();
        ArrayList<Document> docSources = new ArrayList<Document>();

        try {
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();

            for( String fname : patternFiles ) {
                File f = new File( fname );
                if( f.exists() ) {
                    docSources.add( db.parse( fname ) );
                } else {
                    context.getLog()
                            .update( "File \"" + f.getAbsolutePath() + "\" does not exist. Declaration skipped." );
                }
            }
            
            patternRepository.harvestPatterns( docSources.toArray( new Document[0] ), true );

        } catch ( ParserConfigurationException ex ) {
            context.getLog().update( "Parser Configuration Exception occurred. Extraction of patterns aborted." );
        } catch ( SAXException ex ) {
            context.getLog().update( "SAXE Exception occurred while parsing pattern file. Extraction of patterns aborted." );
        } catch ( IOException ex ) {
            context.getLog().update( "IO Exception occurred while parsing pattern file. Extraction of patterns aborted." );
        } catch( XPathExpressionException ex ) {
            ex.printStackTrace();
        }
    }

    public void patternsLoaded() {
        
    }

    public void patternDataChanged() {
        
    }

    public void patternSelected( Pattern p ) {
        selectedPatterns.put( p.getType(), p );
    }
    //</editor-fold>
}
