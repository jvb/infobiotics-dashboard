
package propertybuilder.pattern;

import java.util.ArrayList;
import java.util.Hashtable;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathExpressionException;
import org.w3c.dom.Node;
import propertybuilder.xml.XML;

/**
 *
 * @author Ciprian
 */
public class Pattern implements XML {

    private String name;
    private String id;
    private String patternClass;
    private PatternType type;
    private String description;
    private String question;
    private SymbolSequence template;
    private ArrayList<Translation> translations;
    private Hashtable<String, Variable> variables;

    public Pattern() {
        translations = new ArrayList<Translation>();
        template = new SymbolSequence();
        variables = new Hashtable<String, Variable>();
    }

    public void setName( String name ) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    public void setId( String id ) {
        this.id = id;
    }

    public String getId() {
        return this.id;
    }

    public void setPatternClass( String pclass ) {
        this.patternClass = pclass;
    }

    public String getPatternClass() {
        return this.patternClass;
    }

    public void setPatternType( PatternType type ) {
        this.type = type;
    }

    public void setPatternType( String type ) {
        if( type.equals( "property" ) ) {
            this.type = PatternType.PROPERTY;
        } else if( type.equals( "state" ) ) {
            this.type = PatternType.STATE;
        } else if( type.equals( "reward" ) ) {
            this.type = PatternType.REWARD;
        } else {
            this.type = PatternType.UNDEFINED;
        }
    }

    public PatternType getType() {
        return this.type;
    }

    public void setDescription( String description ) {
        this.description = description;
    }

    public String getDescription() {
        return this.description;
    }

    public void setQuestion( String question ) {
        this.question = question;
    }

    public String getQuestion() {
        return question;
    }

    public void setTemplate( String template ) {
        this.template.parseSequence( template );
    }

    public SymbolSequence getTemplate() {
        return this.template;
    }

    public void addTranslation( Translation t ) {
        this.translations.add( t );
    }

    public void removeTranslation( Translation t ) {
        this.translations.remove( t );
    }

    public int getTranslationsCount() {
        return this.translations.size();
    }

    public void clearTranslations() {
        this.translations.clear();
    }

    public void setVariable( Variable v ) {
        variables.put( v.getId(), v );
    }

    public Variable getVariable( String varId ) {
        return variables.get( varId );
    }

    /* This method is currently incomplete (does not take all necessary
     * data from the xml node). The pattern extraction currently takes
     * place within the PatternRepository object.
     */
    public void fromXML( Node source, XPath xp ) throws XPathExpressionException {
        setName( xp.evaluate( "@name", source ) );
        setId( xp.evaluate( "@id", source ) );
        setPatternClass( xp.evaluate( "@class", source ) );
        setPatternType( xp.evaluate( "@type", source ) );

        //allow descriptions to be declared either as attributes or in separate elements
        String desc = xp.evaluate( "@description", source );
        if( desc == null ) {
            desc = xp.evaluate( "/description/text()", source );
        }
        setDescription( desc );
        setQuestion( xp.evaluate( "/question/text()", source ) );
        
    }

    public String toXML() {
        StringBuffer buf = new StringBuffer();

        buf.append( "<pattern id=\"" + this.getId() + "\" name=\"" + this.getName() + "\" " );
        buf.append( "type=\"" + this.getType().toString() + "\" class=\"" + this.patternClass + "\">" );
        buf.append( XML.lineSep );
        buf.append( "\t<description>" + this.getDescription() + "</description>" );
        buf.append( XML.lineSep );
        buf.append( "\t<question>" + this.getQuestion() + "</question>" );
        buf.append( XML.lineSep );
        buf.append( "</pattern>" );

        return buf.toString();
    }
}
