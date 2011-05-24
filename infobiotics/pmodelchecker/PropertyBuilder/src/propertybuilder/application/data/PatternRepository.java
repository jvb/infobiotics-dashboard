
package propertybuilder.application.data;

import java.util.EnumMap;
import java.util.HashMap;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import propertybuilder.application.ApplicationContext;
import propertybuilder.pattern.Pattern;
import propertybuilder.pattern.PatternType;
import propertybuilder.pattern.Translation;
import propertybuilder.pattern.Variable;

/**
 *
 * @author Ciprian
 */
public class PatternRepository {
    
    private EnumMap<PatternType, PatternDataModel> patternData;
    private ApplicationContext ctx;

    public PatternRepository() {
        init();
    }

    public PatternRepository( ApplicationContext ctx ) {
        setApplicationContext( ctx );
        init();
    }

    private void init() {
        patternData = new EnumMap<PatternType, PatternDataModel>(PatternType.class);
    }

    public void setApplicationContext( ApplicationContext ctx ) {
        this.ctx = ctx;
    }

    public ApplicationContext getApplicationContext() {
        return this.ctx;
    }

    public void addPattern( Pattern pattern ) {
        PatternType type = pattern.getType();
        PatternDataModel model = patternData.get( type );
        if( model == null ) {
            model = new DefaultPatternDataModel( type );
            patternData.put( type, model );
        }
        model.addPattern( pattern );
    }

    public void removePattern( Pattern pattern ) {
        PatternType type = pattern.getType();
        PatternDataModel model = patternData.get( type );
        if( model != null ) {
            model.removePattern( pattern );
        }
    }

    public void updateModels() {
        for( PatternDataModel model : patternData.values() ) {
            model.updateModel();
        }
    }

    public PatternType[] getPatternTypes() {
        return patternData.keySet().toArray( new PatternType[0] );
    }

    public String[] getPatternClasses( PatternType type ) {
        PatternDataModel model = patternData.get( type );
        if( model != null ) {
            return model.getPatternClasses();
        }

        return null;
    }

    public PatternDataModel getModel( PatternType type, boolean create ) {
        PatternDataModel model = patternData.get( type );
        if( model == null && create ) {
            model = new DefaultPatternDataModel( type );
        }

        return model;
    }

    public int getPatternCount( PatternType type ) {
        if( type == null ) {
            return getPatternCount();
        }

        PatternDataModel model = patternData.get( type );
        if( model == null ) {
            return 0;
        }

        return model.getPatternCount();
    }

    public int getPatternCount() {
        int count = 0;
        for( PatternDataModel model : patternData.values() ) {
            count += model.getPatternCount();
        }

        return count;
    }

    public void harvestPatterns( Document[] xmlSources, boolean append ) throws XPathExpressionException {
        if( !append ) {
            for( PatternDataModel model : this.patternData.values() ) {
                model.clearModel();
            }
        }
        
        XPathFactory xpf = XPathFactory.newInstance();
        XPath xp = xpf.newXPath();
        XPathExpressionsFactory xf = new XPathExpressionsFactory( xp );
        for( Document doc : xmlSources ) {
            NodeList rootNodes = (NodeList)
                    xp.evaluate( "/listOfPatterns/pattern", doc, XPathConstants.NODESET );
            int length = rootNodes.getLength();
            for( int i = 0; i < length; i++ ) {
                Node rootNode = rootNodes.item( i );
                harvestPatternData ( rootNode, xf );
            }
        }

        updateModels();
        if( this.ctx != null ) {
            this.ctx.firePatternsLoaded();
        }
    }

    private void harvestPatternData( Node rootNode, XPathExpressionsFactory xf ) throws XPathExpressionException {
        String patternName = xf.getExpression( "name" ).evaluate( rootNode );
        String patternType = xf.getExpression( "type" ).evaluate( rootNode );
        String patternClass = xf.getExpression( "class" ).evaluate( rootNode );
        String patternId = xf.getExpression( "id" ).evaluate( rootNode );
        String description = xf.getExpression( "description inline" ).evaluate( rootNode );
        //the description specified as attribute overrides the element
        if( description == null || description.isEmpty() ) {
            description = xf.getExpression( "description" ).evaluate( rootNode );
        }
        String question = xf.getExpression( "question" ).evaluate( rootNode );
        String template = xf.getExpression( "template" ).evaluate( rootNode );
        Pattern p = new Pattern();
        p.setId( patternId );
        p.setName( patternName );
        p.setPatternType( patternType );
        p.setPatternClass( patternClass );
        p.setDescription( description );
        p.setQuestion( question );
        p.setTemplate( template );
        addPattern( p );

        NodeList translations = (NodeList) xf.getExpression( "translations" )
                .evaluate( rootNode, XPathConstants.NODESET );
        int translationsLength = translations.getLength();
        for( int i = 0; i < translationsLength; i++ ) {
            Node translationNode = translations.item( i );
            String translationTarget = xf.getExpression( "translation target" )
                    .evaluate( translationNode );
            String translationDescription = xf.getExpression( "translation description inline" )
                    .evaluate( translationNode );
            if( translationDescription == null || translationDescription.isEmpty() ) {
                translationDescription = xf.getExpression( "translation description" )
                    .evaluate( translationNode );
            }
            String translationValue = xf.getExpression( "translation value" )
                    .evaluate( translationNode );
            
            p.addTranslation( new Translation( translationTarget,
                    translationDescription, translationValue ) );
        }

        NodeList variables = (NodeList) xf.getExpression( "variables" )
                .evaluate( rootNode, XPathConstants.NODESET );
        int variablesLength = variables.getLength();
        for( int i = 0; i < variablesLength; i++ ) {
            Node variableNode = variables.item( i );
            String varId = xf.getExpression( "variable id" ).evaluate( variableNode );
            String varType = xf.getExpression( "variable type" ).evaluate( variableNode );
            String varInitValue = xf.getExpression( "variable initValue" ).evaluate( variableNode );
            String varDescription = xf.getExpression( "description inline" ).evaluate( variableNode );
            if( varDescription == null || varDescription.isEmpty() ) {
                varDescription = xf.getExpression( "variable description" )
                        .evaluate( variableNode );
            }
            Variable v = p.getTemplate().getVariable( varId );
            if( v != null ) {
                v.setType( varType );
                v.setInitValue( varInitValue );
                v.setDescription( varDescription );
            }
        }
    }

    private class XPathExpressionsFactory {

        private XPath xp;
        public XPathExpression nameExp;
        public XPathExpression typeExp;
        public XPathExpression classExp;
        public XPathExpression idExp;
        public XPathExpression inlineDescriptionExp;
        public XPathExpression descriptionExp;
        public XPathExpression questionExp;
        public XPathExpression templateExp;
        public XPathExpression translationsExp;
        public XPathExpression translationTargetExp;
        public XPathExpression translationDescriptionExp;
        public XPathExpression inlineTranslationDescriptionExp;
        public XPathExpression translationValueExp;
        public XPathExpression variablesExp;
        public XPathExpression variableIdExp;
        public XPathExpression variableTypeExp;
        public XPathExpression variableInitValueExp;
        public XPathExpression variableDescriptionExp;
        public XPathExpression variableInlineDescriptionExp;

        public XPathExpressionsFactory( XPath xp ) throws XPathExpressionException {
            this.xp = xp;

            nameExp = xp.compile( "@name" );
            typeExp = xp.compile( "@type" );
            classExp = xp.compile( "@class" );
            idExp = xp.compile( "@id" );
            inlineDescriptionExp = xp.compile( "@description" );
            descriptionExp = xp.compile( "description/text()" );
            questionExp = xp.compile( "question/text()" );
            templateExp = xp.compile( "template/text()" );
            translationsExp = xp.compile( "translations/translation" );
            translationTargetExp = xp.compile( "@target" );
            translationDescriptionExp = xp.compile( "description/text()" );
            inlineTranslationDescriptionExp = xp.compile( "@description" );
            translationValueExp = xp.compile( "value/text()" );
            variablesExp = xp.compile( "variables/var" );
            variableIdExp = xp.compile( "@id" );
            variableTypeExp = xp.compile( "@type" );
            variableInitValueExp = xp.compile( "@initValue" );
            variableDescriptionExp = xp.compile( "description/text()" );
            variableInlineDescriptionExp = xp.compile( "@description" );
        }
        
        public XPathExpression getExpression( String propertyName ) {

            if( propertyName.equals( "name" ) ) {
                return this.nameExp;
            } else if( propertyName.equals( "type" )) {
                return this.typeExp;
            } else if( propertyName.equals( "class" ) ) {
                return this.classExp;
            } else if( propertyName.equals( "id" )) {
                return this.idExp;
            } else if( propertyName.equals( "description" ) ) {
                return this.descriptionExp;
            } else if( propertyName.equals( "description inline" ) ) {
                return this.inlineDescriptionExp;
            } else if( propertyName.equals( "question" ) ) {
                return this.questionExp;
            } else if( propertyName.equals( "template" ) ) {
                return this.templateExp;
            } else if( propertyName.equals( "translations" ) ) {
                return this.translationsExp;
            } else if( propertyName.equals( "translation target" ) ) {
                return this.translationsExp;
            } else if( propertyName.equals( "translation description" ) ) {
                return this.translationDescriptionExp;
            } else if( propertyName.equals( "translation description inline" ) ) {
                return this.inlineTranslationDescriptionExp;
            } else if( propertyName.equals( "translation value" ) ) {
                return this.translationValueExp;
            } else if( propertyName.equals( "variables" ) ) {
                return this.variablesExp;
            } else if( propertyName.equals( "variable id" ) ) {
                return this.variableIdExp;
            } else if( propertyName.equals( "variable type" ) ) {
                return this.variableTypeExp;
            } else if( propertyName.equals( "variable initValue" ) ) {
                return this.variableInitValueExp;
            } else if( propertyName.equals( "variable description" ) ) {
                return this.variableDescriptionExp;
            } else if( propertyName.equals( "variable description inline" ) ) {
                return this.variableInlineDescriptionExp;
            }

            return null;
        }
    }
}
